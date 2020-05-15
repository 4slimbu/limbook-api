from flask import request, current_app


def filter_model(model, filters, count_only=False):
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('PAGINATION')
    start = (page - 1) * per_page

    # query building
    query = model.query
    for f in filters.values():
        if f:
            query = query.filter(f)

    # if count_only
    if count_only:
        return query.count()

    query = query.order_by(model.created_on).limit(per_page).offset(start)

    return query.all()
