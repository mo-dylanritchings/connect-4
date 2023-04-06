from constructs import Construct

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

from cdk_dynamo_table_view import TableViewer
from .win_counter import WinCounter
#from .win_getter import WinGetter

class ScoreboardStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #ADD

        win_add_reply = _lambda.Function(
            self, 'WinReplyHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='win_reply.handler',
        )

        scoreboard_win_counter = WinCounter(
            self, 'ScoreboardWinCounter',
            downstream=win_add_reply,
        )

        #creates endpoint
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=scoreboard_win_counter._handler,
        )

        #GET

        win_get_reply = _lambda.Function(
            self, 'WinGetHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='win_get_reply.handler',
        )

        scoreboard_win_getter= WinCounter(
            self, 'ScoreboardWinGetter',
            downstream=win_get_reply,
        )


        #creates endpoint
        apigw.LambdaRestApi(
            self, 'GetEndpoint',
            handler=scoreboard_win_getter._getter,
        )

        # win_get_reply = _lambda.Function(
        #     self, 'WinGetHandler',
        #     runtime=_lambda.Runtime.PYTHON_3_7,
        #     code=_lambda.Code.from_asset('lambda'),
        #     handler='win_get_reply.handler',
        # )

        # scoreboard_win_getter= WinGetter(
        #     self, 'ScoreboardWinGetter',
        #     downstream=win_get_reply,
        # )


        # #creates endpoint
        # apigw.LambdaRestApi(
        #     self, 'GetEndpoint',
        #     handler=scoreboard_win_getter._handler,
        # )


        #TABLE

        TableViewer(
            self, 'ViewScoreboard',
            title='Scoreboard',
            table=scoreboard_win_counter.table,
            sort_by='-wins'
        )

