from price_check.figures import bp
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request, session
from price_check.models import FiguresDetails
from price_check.figures.figures_service import find_figures_details_sorted_filtered, find_max_price, find_min_price, find_avg_price, find_last_date, \
find_by_id, find_figures_details_sorted_filtered_all, find_figures_with_base_stats, filter_all_columns_by_value

ROWS_PER_PAGE=10

@bp.route('/market/figures', methods=['GET', 'POST'])
def figures_page():

    if request.method == 'POST':
        session['selected_filter_option'] = request.form.get('filtered_by', "All")
        session['selected_option'] = request.form.get('sorted_by', "price_asc")
        session['find_part'] = request.form.get('find_part', "")
        return redirect(url_for('figures.figures_page'))

    page = request.args.get('page', 1, type=int)
    filter_options = ["All", "MTG", "FGB"]
    filters = {}
    last_date = find_last_date()
    filters['download'] = last_date
    selected_filter_option = session.get('selected_filter_option', "All")
    if selected_filter_option == 'All':
        filters.pop("source", None)
    else:
        filters['source'] = selected_filter_option
    selected_option = session.get('selected_option', "price_asc")
    selected_field = selected_option.split("_")[0]
    selected_order = selected_option.split("_")[1]
    find_part = session.get('find_part',"")

    selection_options=["title_asc", "title_desc", "price_asc", "price_desc", "availability_asc", "availability_desc"]
    figures_details_pagin = find_figures_with_base_stats(selected_field, selected_order, find_part, filters, page, ROWS_PER_PAGE)
    return render_template('figures/figures.html',
                           figures_details_pagin=figures_details_pagin,
                           selection_options=selection_options,
                           selected_option=selected_option,
                           filter_options=filter_options,
                           selected_filter_option=selected_filter_option,
                           find_part=find_part)


@bp.route('/market/figures/<id>', methods=['GET'])
def figures_details_page(id):

    figure = find_by_id(id)
    filters = {}

    filters['title'] = figure.title
    filters['source'] = figure.source

    page = request.args.get('page', 1, type=int)
    selected_option = "download_asc"
    selected_field = selected_option.split("_")[0]
    selected_order = selected_option.split("_")[1]

    figures_details_pagin = find_figures_details_sorted_filtered(selected_field, selected_order ,filters, page, ROWS_PER_PAGE)
    figures_details_all = find_figures_details_sorted_filtered_all(selected_field, selected_order ,filters)
    
    min_price = find_min_price(filters)
    max_price = find_max_price(filters)
    avg_price = find_avg_price(filters)

    return render_template('figures/figures_details.html',figure=figure, figures_details_pagin=figures_details_pagin, figures_details_all=figures_details_all, min_price=min_price, max_price=max_price, avg_price=avg_price)