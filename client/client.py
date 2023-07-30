from playwright.sync_api import sync_playwright

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

    entries = []
    for entry in content[1:]:
        split = list(
            map(str.strip,
                filter(None, entry.split(sep='\t'))
                )
        )

        entries.append(
            FerryScheduleEntry(
                sailing_time=split[0],
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
