import pyautogui
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, GiftEvent
from TikTokLive.proto.custom_proto import ExtendedGiftStruct

gifts_dict = {"chocolate": "1",
              "ice_cream": "2",
              "rose": "3",
              "soccer": "4"}

client: TikTokLiveClient = TikTokLiveClient(unique_id='@livequizmaster')


@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent) -> None:
    print('Connected to Room ID:', client.room_id)


@client.on(GiftEvent)
async def on_gift(event: GiftEvent) -> None:
    # If it's type 1 and the streak is over
    if event.gift.info.type == 1:
        if event.gift.is_repeating == 1:
            parse_gifts(event.gift, n=event.repeat_count)
            print(f"{event.user.unique_id} sent {
                  event.repeat_count}x \"{event.gift.name}\"")

    # It's not type 1, which means it can't have a streak & is automatically over
    elif event.gift.info.type != 1:
        parse_gifts(event.gift)
        print(f"{event.user.unique_id} sent \"{event.gift.name}\"")


def parse_gifts(gift: ExtendedGiftStruct, n: int = 1) -> None:
    for _ in range(n):
        pyautogui.keyDown(gifts_dict[gift.name])
        pyautogui.keyUp(gifts_dict[gift.name])


if __name__ == '__main__':
    client.run()
