import boto3
import csv

from tqdm import tqdm


USER_LIST_FILE_NAME = 'unactive_user_df.csv'  # 여기에 파일 이름(확장자 포함) 입력

global cnt_resource_not_found_exception
global cnt_delete_success


def delete_channel(client, channel_arn):
    global cnt_delete_success

    channel_arn = get_channel_arn(client, channel_arn)

    try:
        response = client.delete_signaling_channel(
            ChannelARN=channel_arn
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            cnt_delete_success += 1
    except Exception as e:
        pass


def get_channel_arn(client, channel_name):
    global cnt_resource_not_found_exception
    try:
        response = client.describe_signaling_channel(
            ChannelName=channel_name
        )

        return response['ChannelInfo']['ChannelARN']
    except Exception as e:
        if e.__class__.__name__ == 'ResourceNotFoundException':
            cnt_resource_not_found_exception += 1
        else:
            pass


if __name__ == '__main__':
    client = boto3.client('kinesisvideo')

    try:
        with open(USER_LIST_FILE_NAME, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(reader)  # remove header line

            for row in tqdm(reader):
                channel_name = row[1]
                delete_channel(client, channel_name)

            print('존재하지 않는 Channel 수 :', cnt_resource_not_found_exception)
            print('삭제된 Channel 수 :', cnt_delete_success)
    except Exception as e:
        print(e.__class__)
