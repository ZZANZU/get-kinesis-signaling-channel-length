import boto3


def get_channel_count():
    """
    Kinesis Video(WebRTC)의 Signaling Channel 수 조회
    """
    client = boto3.client('kinesisvideo')
    response = client.list_signaling_channels(
        MaxResults=1000
    )

    total_channel_length = 0

    try:
        while response['NextToken']:
            total_channel_length += len(response['ChannelInfoList'])

            response = client.list_signaling_channels(
                NextToken=response['NextToken']
            )
    except:
        total_channel_length += len(response['ChannelInfoList'])

    return total_channel_length


if __name__ == '__main__':
    print(get_channel_count())
