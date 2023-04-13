from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_dynamodb as dynamodb,
    aws_lambda,
    aws_apigateway as apigw
)

from constructs import Construct

class ScoreboardStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = self.create_ddb()

        table_lambda = self.create_lambda(table)

        table.grant_read_write_data(table_lambda)

        self.create_gateway(table_lambda)


    def create_ddb(self) -> dynamodb.Table:
      return dynamodb.Table(self, "Connect4_Scoreboard_DB",
    partition_key=dynamodb.Attribute(name="player", type=dynamodb.AttributeType.STRING)
                            )


    def create_lambda(self, table) -> aws_lambda.Function:
       return aws_lambda.Function(self, "Connect4_Scoreboard_Lambda",
                                  code=aws_lambda.Code.from_asset("./lambda/"),
                                  runtime=aws_lambda.Runtime.PYTHON_3_8,
                                  environment={
                                      "TABLE_NAME": table.table_name
                                  },
                                  handler="lambda.lambda_handler"
                            )

    def create_gateway(self, table_lambda):
        api = apigw.LambdaRestApi(
            self, "Enpoint",
            handler=table_lambda,
        )
        items = api.root.add_resource("scoreboard")
        items.add_method("GET")
        items.add_method("POST")


