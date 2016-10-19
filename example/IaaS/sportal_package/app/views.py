from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from sportal.service.task import SiteTask
from sportal.service import decorator
from sportal import util
import logging
logger = logging.getLogger(__name__)


@login_required
@decorator.user_service_create_site_auth
def create_site(request, **kwargs):
    service_name = kwargs['service_name']

    if request.method == 'POST':
        task = SiteTask(request.user.id, service_name)
        # *** get site is private, share to all or share to group of users ***
        error_msg, is_private, is_share_to_all, selected_user_list = \
            task.get_share_site_settings(request)
        if error_msg:
            messages.error(request, error_msg)
            return HttpResponseRedirect(reverse(
                util.get_service_create_site_url_name(service_name)))

        extra_params = {
            'instance-private-network': request.POST.get('network'),
            'instance-flavor': request.POST.get('flavor'),
            'instance-image': request.POST.get('image'),
            'instance-number': request.POST.get('num_of_machines')
        }
        status_code, site_obj = task.create_site(
            request.POST.get('site_name'),
            request.POST.get('description'),
            is_private,
            is_share_to_all,
            selected_user_list,
            extra_params)
        if not site_obj:
            messages.error(
                request, _('Create site was failed: status code is {0}'.
                           format(status_code)))

        return HttpResponseRedirect(
            reverse(util.get_service_index_url_name(service_name)))

    # < get create site basic info >
    create_site_info = SiteTask(
        request.user.id, service_name).get_create_site_info()

    # < image and flavor are hardcode now >
    # image
    create_site_info['image'] = ['Ubuntu14.04-2015.3.0',
                                 'Windows7-2015.3.0']
    # flavor
    create_site_info['flavor'] = ['2cores4GBmemory40GBdisk',
                                  '4cores8GBmemory80GBdisk',
                                  '8cores16GBmemory160GBdisk']

    return render(request,
                  'service/{0}/create_site.html'.format(service_name.lower()),
                  create_site_info)


@login_required
@decorator.user_service_site_auth
def detail_view(request, site_id, **kwargs):
    service_name = kwargs['service_name']

    # < get site detail info >
    task = SiteTask(request.user.id, service_name)
    site_detail_info = task.get_detail_site_info(site_id)

    return render(request,
                  'service/{0}/detail.html'.format(service_name.lower()),
                  site_detail_info)
