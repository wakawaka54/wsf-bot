from playwright.sync_api import sync_playwright
import datetime

from client.types import VehicleSize, VehicleHeight, FerryScheduleEntry, FerrySchedule, FerryRequest

WSF_ENDPOINT = 'https://secureapps.wsdot.wa.gov/ferries/reservations/vehicle/SailingSchedule.aspx'

TERMINAL_MAP = {
    'anacortes': '1',
    'friday harbor': '10',
    'coupeville': '11',
    'lopez island': '13',
    'orcas island': '15',
    'port townsend': '17',
    'shaw island': '18'
}

VEHICLE_MAP = {
    VehicleSize.VEHICLE_UNDER_22: '3'
}

VEHICLE_HEIGHT_MAP = {
    VehicleHeight.UP_TO_7_2_TALL: '1000',
    VehicleHeight.FROM_7_2_TO_7_6_TALL: '1001',
    VehicleHeight.FROM_7_6_TO_13_TALL: '6'
}

TIME_FORMAT = '%I:%M %p'

def fetch_ferry_schedule(request: FerryRequest):
    if request.terminal_from not in TERMINAL_MAP:
        raise TypeError(f'Unknown terminal name provided: {request.terminal_from}')

    if request.terminal_from not in TERMINAL_MAP:
        raise TypeError(f'Unknown terminal name provided: {request.terminal_from}')

    with sync_playwright() as playwright:
        chrome = playwright.chromium
        browser = chrome.launch()
        page = browser.new_page()
        page.goto(WSF_ENDPOINT)

        page.locator('#MainContent_dlFromTermList').select_option(value=TERMINAL_MAP[request.terminal_from])
        page.locator('#MainContent_dlToTermList').select_option(value=TERMINAL_MAP[request.terminal_to])

        page.locator('#MainContent_txtDatePicker').type(request.sailing_date.replace('/', ''))
        page.click('body')

        page.locator('#MainContent_dlVehicle').select_option(value=VEHICLE_MAP[request.vehicle_size])
        page.locator('#MainContent_ddlCarTruck14To22').select_option(value=VEHICLE_HEIGHT_MAP[request.vehicle_height])

        page.locator('#MainContent_linkBtnContinue').click()

        page.wait_for_timeout(timeout=1000)

        content = page.locator('#MainContent_gvschedule tr').all_inner_texts()

        page.close()

    sailing_time_from = \
        datetime.datetime.strptime(request.sailing_time_from, TIME_FORMAT).time() if request.sailing_time_from else None

    sailing_time_to = \
        datetime.datetime.strptime(request.sailing_time_to, TIME_FORMAT).time() if request.sailing_time_to else None

    entries = []
    for entry in content[1:]:
        split = list(
            map(str.strip, filter(None, entry.split(sep='\t')))
        )

        sailing_time = datetime.datetime.strptime(split[0], TIME_FORMAT).time()

        if sailing_time_from and sailing_time < sailing_time_from:
            continue

        if sailing_time_to and sailing_time > sailing_time_to:
            continue

        entries.append(
            FerryScheduleEntry(
                sailing_time=sailing_time,
                available=any("Space Available" in s for s in split),
                vessel=split[-1]
            )
        )

    return FerrySchedule(
        sailing_date=request.sailing_date,
        terminal_from=request.terminal_from,
        terminal_to=request.terminal_to,
        entries=entries
    )
