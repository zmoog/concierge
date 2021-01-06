from datetime import date
import logging

from app import config, bootstrap
from app.domain import commands, model

app_logger = logging.getLogger()
app_logger.setLevel(config.LOG_LEVEL)

logger = logging.getLogger(__name__)

whens = {
    'today': date.today,
    'previous_business_day': model.find_previous_business_day
}

messagebus = bootstrap.for_lambda()


def run_scheduled(event, config):
    print(f'running run_scheduled with event {event}')
    if 'Summarize' in event:
        when = event['Summarize'].get('when', 'today')

        if when not in whens:
            print(f'"{when}" is not a supported "when" value ({whens.keys()})')
            return

        day = whens[when]()
        print(f'summarizing {day}')
        cmd = commands.Summarize(day=day)
    if 'SummarizeWorkTypes' in event:
        request = event['SummarizeWorkTypes']
        when = request.get('when', 'today')
        project_ids = request.get('project_ids')

        if when not in whens:
            print(f'"{when}" is not a supported "when" value ({whens.keys()})')
            return

        day = whens[when]()
        print(f'summarizing work items for {day}')

        cmd = commands.SummarizeWorkTypes(since=day,
                                          until=day,
                                          project_ids=project_ids)

    elif 'CheckRefurbished' in event:
        cmd = commands.CheckRefurbished(
            store=event['CheckRefurbished'].get('store', 'it'),
            products=event['CheckRefurbished']['products']
        )
    elif 'DownloadIFQ' in event:
        cmd = commands.DownloadIFQ(
            day=date.today()
        )
    else:
        return

    messagebus.handle(cmd, {})
