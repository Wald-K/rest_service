import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import ipaddress
from .libs.heavy_load import node_library
from .libs.extras import ip_to_binary_list, TagsProvider


logger = logging.getLogger('ip_request_logger')


def show_ip_tags(request, ip_address):
    try:
        ipaddress.IPv4Address(ip_address)
    except:
        data = {'message': 'Invalid IP address in request'}
        logger.error('Invalid IP address in request')
        return JsonResponse(data, status=400)

    if node_library is not None:
        ip_binary = ip_to_binary_list(ip_address)
        tags_provider = TagsProvider(node_library)
        tags = tags_provider.get_tags_for_ip(ip_binary)
        logger.info('Json response sent')
        return JsonResponse(tags, status=200, safe=False)
    else:
        logger.info('Library not loaded')
        data = {'message': 'Library not loaded'}
        return JsonResponse(data, status=400)


def show_ip_tags_report(request, ip_address):
    try:
        ipaddress.IPv4Address(ip_address)
    except:
        data = {'message': 'Invalid IP address in request'}
        logger.error('Invalid IP address in request')
        return render(request, 'ip_library/error_info.html', data, status=400)

    if node_library is not None:
        ip_binary = ip_to_binary_list(ip_address)
        tags_provider = TagsProvider(node_library)
        tags = tags_provider.get_tags_for_ip(ip_binary)
        context = {'ip_address': ip_address, 'tags': tags}
        logger.info('Html response sent')
        return render(request, 'ip_library/report.html', context)
    else:
        logger.info('Library not loaded')
        data = {'message': 'Library not loaded'}
        return render(request, 'ip_library/error_info.html', data)
