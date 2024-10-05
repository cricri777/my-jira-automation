import main


def lambda_handler(event, context):
    main.run()

    return {
        'statusCode': 200,
        'body': 'Run Complete'
    }