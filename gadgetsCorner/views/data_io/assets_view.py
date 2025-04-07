"""This module contains the view for the assets template."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gadgetsCorner.models.assets import FixedAssets
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def assets_view(request):
    """This function returns the assets page."""
    if request.method == 'GET':
        assets = FixedAssets.objects.all()
        paginator = Paginator(assets, 12)
        page_number = request.GET.get("page")
        
        try:
            assets = paginator.page(page_number)
        except PageNotAnInteger:
            assets = paginator.page(1)
        except EmptyPage:
            assets = paginator.page(paginator.num_pages)
        return render(request, 'users/admin_sites/assets.html',
                      {'assets': assets, 'paginator': paginator})
    return redirect('dashboard')


@login_required
def update_asset(request):
    """This function updates the asset."""
    if request.method == 'POST' and request.user.is_superuser:
        asset_id = request.POST.get('assetId')
        asset_name = request.POST.get('assetName')
        asset_cost = request.POST.get('assetCost')
        asset_description = request.POST.get('assetDescription')
        asset_life = request.POST.get('assetLife')
        asset_date = request.POST.get('assetDate')

        try:
            asset = FixedAssets.objects.get(id=asset_id)
            asset.name = asset_name
            asset.cost = asset_cost
            asset.description = asset_description
            asset.date_purchased = asset_date
            asset.useful_life = asset_life
            asset.save()
            messages.success(request, 'Asset updated successfully.')
        except FixedAssets.DoesNotExist:
            messages.error(request, 'Asset not found.')
        except Exception as e:
            messages.error(request, f'Error updating asset: {e}')
    return redirect('assets_view')


@login_required
def delete_asset(request):
    """This function deletes the asset."""
    if request.method == 'POST' and request.user.is_superuser:
        asset_id = request.POST.get('assetId')

        try:
            asset = FixedAssets.objects.get(id=asset_id)
            asset.delete()
            messages.success(request, 'Asset deleted successfully.')
        except FixedAssets.DoesNotExist:
            messages.error(request, 'Asset not found.')
        except Exception as e:
            messages.error(request, f'Error deleting asset: {e}')
    return redirect('assets_view')