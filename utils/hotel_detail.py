from typing import Dict, Optional, List
import json

from .request_to_api import request_to_api
from .value_from_multidict import value_from_mutidict
from config_data.config import RAPID_API_KEY


def hotel_detail(hotels: List[dict], photos_amount: int) \
        -> Optional[List[dict]]:
    """
    Дополняет данные по отелям адресом и фотографиями

    :param hotels: список отелей
    :param photos_amount: количество фотографий
    :return: список отелей
    """
    if hotels is None:
        return None

    url = 'https://hotels4.p.rapidapi.com/properties/v2/detail'

    payload = {
        'currency': 'USD',
        'eapid': 1,
        'locale': 'ru_RU',
        'siteId': 300000001
    }
    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': RAPID_API_KEY,
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    }

    for index, hotel in enumerate(hotels):
        payload['propertyId'] = hotel['hotel_id']
        response = request_to_api(method='POST', url=url, headers=headers,
                                  json=payload)
        hotels[index]['photos_list'] = list()
        address = None
        if response:
            result = json.loads(response)
            address = value_from_mutidict(result, ['data', 'propertyInfo',
                                                   'summary', 'location',
                                                   'address', 'addressLine'])
            images = value_from_mutidict(result, ['data', 'propertyInfo',
                                                  'propertyGallery', 'images'])
            if images is None:
                images = list()
            count = 0
            for image in images:
                count += 1
                if count > photos_amount:
                    break
                hotels[index]['photos_list'].append(image['image']['url'])

        hotels[index]['address'] = address

    return hotels