from discord_webhook import DiscordWebhook

from notifications.types import FoundAvailableNotification


def send_notification(notification: FoundAvailableNotification, webhook: str):
    schedule = notification.schedule
    lines = [
        f'🚨 Found available ferry routes on {schedule.sailing_date} ' +
        f'from {schedule.terminal_from} to {schedule.terminal_to}:'
    ]

    for entry in schedule.entries:
        if entry.available:
            lines.append(f'{entry.sailing_time} {entry.vessel}')

    lines.append(
        'Follow this link to reserve. https://secureapps.wsdot.wa.gov/ferries/reservations/vehicle/SailingSchedule.aspx'
    )

    message = '\n'.join(lines)

    print(f'Sending discord message to {webhook}:\n{message}')

    DiscordWebhook(url=webhook, content=message).execute()
