from flask import request, current_app


def filter_model(model, query, count_only=False):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get(
        'per_page', current_app.config.get('PAGINATION'), type=int)
    start = (page - 1) * per_page

    # if count_only
    if count_only:
        return query.count()

    query = query.order_by(model.created_on).limit(per_page).offset(start)

    return query.all()
