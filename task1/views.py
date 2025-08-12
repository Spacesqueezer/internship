from datetime import datetime
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_start=True, set_cookie=True)
def index(request):
    return render(request, 'index.html', {'user': request.bitrix_user})

@main_auth(on_cookies=True)
def get_last_deals(request):

	print('get_last_deals')

	# Задаём параметры для получения сделок
	params = {
		"filter": {
			"STAGE_SEMANTIC_ID": "P" # Получение активных сделок
		},
		"select": ["TITLE", # Название
				   "STAGE_ID", # Стадия
				   "DATE_CREATE", # Дата создания
				   "OPPORTUNITY" # Сумма
				   ],
		"order": {"DATE_CREATE": "DESC"},
	}

	print('params: ', params)

	# Получаем список последних сделок
	response = request.bitrix_user_token.call_api_method('crm.deal.list', params)
	deals = response.get('result', [])[:10]

	# Преобразуем дату
	for deal in deals:
		raw_date = deal.get("DATE_CREATE")
		dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
		deal["DATE_CREATE"] = dt.strftime("%d.%m.%Y %H:%M")

	return render(request, 'last_deals.html', {'deals': deals})
