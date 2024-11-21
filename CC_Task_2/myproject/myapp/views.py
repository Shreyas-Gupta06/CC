from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .utils import read_ids
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), 'bits_ids.txt')
ids = read_ids(FILE_PATH)

def id_details(request, uid):
    # Find the full ID by searching for the partial UID (last 4 digits)
    matching_ids = [id for id in ids if id[8:12] == uid]

    if not matching_ids:
        return JsonResponse({'error': 'No matching ID found for the given UID'}, status=404)

    # Assuming we want to return details for the first match
    full_id = matching_ids[0]
    x = 'Pilani' if full_id.endswith('P') else 'Goa' if full_id.endswith('G') else 'Hyderabad' if full_id.endswith('H') else 'Unknown'

    # Extract details based on the full ID
    details = {
        'id': full_id,
        'uid': full_id[8:12],  # UID is the last 4 digits
        'email': f'f{full_id}@{x}.bits-pilani.ac.in',
        'branch': full_id[4:6],
        'year': 2025 - int(full_id[:4]),
        'campus': x
    }

    return JsonResponse(details)

def filter_by_query(request):
    # Get query parameters
    current_branch = request.GET.get('branch')
    current_year = request.GET.get('year')
    x = request.GET.get('format')

    filtered_ids = ids  # Start with all IDs

    # Filter by branch if the 'branch' parameter is provided
    if current_branch:
        branch_mapping = {
            'chemical': 'A1', 'civil': 'A2', 'eee': 'A3', 'mech': 'A4',
            'pharma': 'A5', 'biotech': 'A6', 'cs': 'A7', 'eni': 'A8',
            'bio': 'B1', 'chem':'B2', 'eco': 'B3', 'math': 'B4', 'phy': 'B5',
            'ece': 'B5', 'genstudies': 'GS','manu':'AB',
        }

        if current_branch in branch_mapping:
            filtered_ids = [id for id in filtered_ids if id[4:6] == branch_mapping[current_branch]]
        else:
            return JsonResponse({'error': 'No matching branch found'}, status=404)

    # Filter by year if the 'year' parameter is provided
    if current_year:
        try:
            current_year = int(current_year)
            filtered_ids = [id for id in filtered_ids if (2025 - int(id[:4])) == current_year]
        except ValueError:
            return JsonResponse({'error': 'Invalid year parameter'}, status=400)

    # If 'format' is 'text', return all IDs as plain text
    if x == 'text':
        return HttpResponse('\n'.join(filtered_ids), content_type='text/plain')

    # Default: Return filtered IDs as JSON
    return JsonResponse({'ids': filtered_ids})

