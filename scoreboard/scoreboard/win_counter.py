from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    RemovalPolicy
)

class WinCounter(Construct):

    @property
    def handler(self):
        return self._handler

    @property
    def getter(self):
        return self._getter

    @property
    def table(self):
        return self._table

    def __init__(self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._table = ddb.Table(
            self, 'Wins',
            partition_key={'name': 'user', 'type': ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY
        )

        self._handler = _lambda.Function(
            self, 'WinCountHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='win_count.handler',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                'WIN_TABLE_NAME': self._table.table_name,
            }
        )

        self._getter = _lambda.Function(
            self, 'WinGetHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='win_get.getter',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                'WIN_TABLE_NAME': self._table.table_name,
            }
        )

        self._table.grant_read_write_data(self.getter)
        self._table.grant_read_write_data(self.handler)
        downstream.grant_invoke(self.getter)
        downstream.grant_invoke(self.handler)
