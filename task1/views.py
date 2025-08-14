import pprint
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_start=True, set_cookie=True)
def index(request):
	return render(request, 'index.html', {'user': request.bitrix_user})

@main_auth(on_cookies=True)
def get_last_deals(request):
	# Задаём параметры для получения сделок
	params = {
		"filter": {
			"STAGE_SEMANTIC_ID": "P" # Получение активных сделок
		},
		"select": ["TITLE",              # Название
				   "STAGE_ID",           # Стадия
				   "DATE_CREATE",        # Дата создания
				   "OPPORTUNITY",        # Сумма
				   "UF_CRM_1755065188"   # Кастомный текст
				   ],
		"order": {"DATE_CREATE": "DESC"},
	}

	# Получаем список последних сделок
	response = request.bitrix_user_token.call_api_method('crm.deal.list', params)
	deals = response.get('result', [])[:10]

	# Преобразуем дату
	for deal in deals:
		raw_date = deal.get("DATE_CREATE")
		dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
		deal["DATE_CREATE"] = dt.strftime("%d.%m.%Y %H:%M")

	return render(request, 'last_deals.html', {'deals': deals})

@main_auth(on_cookies=True)
def create_deal(request):
	if request.method == 'POST':
		# Получаем данные из формы
		title = request.POST.get('title')
		price = request.POST.get('price')
		custom_text = request.POST.get('custom_text')

		try:
			# Создаем сделку
			response = request.bitrix_user_token.call_api_method('crm.deal.add', {
				"fields": {
					"TITLE": title,                     # Название
					"OPPORTUNITY": price,               # Сумма сделки
					"STAGE_ID": "NEW",                  # Этап "Новая"
					"UF_CRM_1755065188": custom_text    # Кастомный текст
				}
			})

			# Возвращаем ID новой сделки
			return JsonResponse({"result": "ok", "deal_id": response.get('result')})

		except Exception as e:
			return JsonResponse({"result": "error", "message": str(e)}, status=500)

	return JsonResponse({"result": "error", "message": "Метод не поддерживается"}, status=405)

