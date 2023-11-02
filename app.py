from flask import Flask, render_template, request
from flask_paginate import Pagination
from db_handler import execute_query


app = Flask(__name__)

@app.route('/')
def homepage():
    select_query = "SELECT id,name FROM category"
    categories = execute_query(select_query)
    select_query = "SELECT id,name FROM nation"
    nations = execute_query(select_query)
    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id ORDER BY RAND()LIMIT 5"
    nominates = execute_query(select_query)
    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id ORDER BY movie.created_at DESC LIMIT 16"
    newest = execute_query(select_query)
    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE nation.name = 'Hàn Quốc' LIMIT 8"
    koreans = execute_query(select_query)
    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE nation.name = 'Trung Quốc' LIMIT 8"
    chinese = execute_query(select_query)
    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE nation.name = 'Thái Lan' LIMIT 8"
    thailands = execute_query(select_query)
    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE publish_status.name = 'Sắp chiếu' ORDER BY RAND()LIMIT 5"
    upcomings = execute_query(select_query)
    return render_template('index.html', categories=categories, nations=nations,nominates=nominates,newest=newest,koreans=koreans,chinese=chinese,thailands=thailands,upcomings=upcomings)

@app.route('/the-loai/<id>', methods=['GET'])
def category(id):
    select_query = "SELECT id,name FROM category"
    categories = execute_query(select_query)
    select_query = "SELECT id,name FROM nation"
    nations = execute_query(select_query)
    select_query = f"SELECT name FROM category WHERE id = {id}"
    category = execute_query(select_query)[0][0]

    page = request.args.get('page', default=1, type=int)

    movie_per_page = 32
    offset = (page - 1) * movie_per_page

    select_query = f"SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id WHERE movie.categories LIKE '{category}' LIMIT {offset}, {movie_per_page}"
    movies = execute_query(select_query)
    movie_count = len(movies)

    total_page = movie_count // movie_per_page + 1

    pagination = Pagination(page=page, per_page=movie_per_page, total=movie_count, css_framework='bootstrap4')

    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE publish_status.name = 'Sắp chiếu' ORDER BY RAND()LIMIT 5"
    upcomings = execute_query(select_query)
    
    return render_template('theloai.html',categories=categories,nations=nations,category=category,page=page,total_page=total_page,movies=movies,upcomings=upcomings,pagination=pagination)

@app.route('/quoc-gia/<id>', methods=['GET'])
def nation(id):
    select_query = "SELECT id,name FROM category"
    categories = execute_query(select_query)
    select_query = "SELECT id,name FROM nation"
    nations = execute_query(select_query)
    page = request.args.get('page', default=1, type=int)

    select_query = f"SELECT name FROM nation WHERE id = {id}"
    nation = execute_query(select_query)[0][0]

    movie_per_page = 32
    offset = (page - 1) * movie_per_page

    select_query = f"SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id WHERE movie.nation = {id} LIMIT {offset}, {movie_per_page}"
    movies = execute_query(select_query)
    
    movie_count = len(movies)

    total_page = movie_count // movie_per_page + 1

    pagination = Pagination(page=page, per_page=movie_per_page, total=movie_count, css_framework='bootstrap4')

    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE publish_status.name = 'Sắp chiếu' ORDER BY RAND()LIMIT 5"
    upcomings = execute_query(select_query)
    
    return render_template('quocgia.html',categories=categories,nations=nations,nation=nation,page=page,total_page=total_page,movies=movies,upcomings=upcomings,pagination=pagination)

@app.route('/xem-phim/<id>', methods=['GET'])
def movie(id):
    select_query = "SELECT id,name FROM category"
    categories = execute_query(select_query)
    select_query = "SELECT id,name FROM nation"
    nations = execute_query(select_query)
    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE publish_status.name = 'Sắp chiếu' ORDER BY RAND()LIMIT 5"
    upcomings = execute_query(select_query)
    select_query = f"SELECT movie.id,movie.name_vn,movie.name_en,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(lang.name, 'DefaultValue') AS lang,COALESCE(nation.name, 'DefaultValue') AS nation,movie.duration,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.source,movie.thumbnail,movie.created_at,movie.categories,movie.actors,COALESCE(series.name, 'DefaultValue') AS series FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN lang ON movie.lang = lang.id LEFT JOIN nation ON movie.nation = nation.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN series ON movie.series = series.id WHERE movie.id = {id}"
    movie = execute_query(select_query)[0]
    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id ORDER BY RAND()LIMIT 5"
    nominates = execute_query(select_query)

    return render_template('phimchitiet.html', movie=movie,categories=categories,nations=nations,upcomings=upcomings,nominates=nominates)


@app.route('/trinh-xem-phim/<id>', methods=['GET'])
def playmovie(id):
    select_query = "SELECT id,name FROM category"
    categories = execute_query(select_query)
    select_query = "SELECT id,name FROM nation"
    nations = execute_query(select_query)
    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE publish_status.name = 'Sắp chiếu' ORDER BY RAND()LIMIT 5"
    upcomings = execute_query(select_query)
    select_query = f"SELECT movie.id,movie.name_vn,movie.name_en,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(lang.name, 'DefaultValue') AS lang,COALESCE(nation.name, 'DefaultValue') AS nation,movie.duration,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.source,movie.thumbnail,movie.created_at,movie.categories,movie.actors,COALESCE(series.name, 'DefaultValue') AS series FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN lang ON movie.lang = lang.id LEFT JOIN nation ON movie.nation = nation.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN series ON movie.series = series.id WHERE movie.id = {id}"
    movie = execute_query(select_query)[0]
    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id ORDER BY RAND()LIMIT 5"
    nominates = execute_query(select_query)
    select_query = f"SELECT id,name_vn FROM movie WHERE series = (SELECT series FROM movie WHERE id = {id} AND series NOT IN (1,2))"
    episodes = execute_query(select_query)

    return render_template('trinhxemphim.html', movie=movie,categories=categories,nations=nations,upcomings=upcomings,nominates=nominates,episodes=episodes)

@app.route('/phim-le', methods=['GET'])
def singlemovie():
    select_query = "SELECT id,name FROM category"
    categories = execute_query(select_query)
    select_query = "SELECT id,name FROM nation"
    nations = execute_query(select_query)

    page = request.args.get('page', default=1, type=int)

    movie_per_page = 32
    offset = (page - 1) * movie_per_page

    select_query = f"SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id WHERE movie.series = 1 LIMIT {offset}, {movie_per_page}"
    movies = execute_query(select_query)
    movie_count = len(movies)

    total_page = movie_count // movie_per_page + 1

    pagination = Pagination(page=page, per_page=movie_per_page, total=movie_count, css_framework='bootstrap4')

    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE publish_status.name = 'Sắp chiếu' ORDER BY RAND()LIMIT 5"
    upcomings = execute_query(select_query)
    
    return render_template('phimle.html',categories=categories,nations=nations,page=page,total_page=total_page,movies=movies,upcomings=upcomings,pagination=pagination)

@app.route('/phim-chieu-rap', methods=['GET'])
def theatermovie():
    select_query = "SELECT id,name FROM category"
    categories = execute_query(select_query)
    select_query = "SELECT id,name FROM nation"
    nations = execute_query(select_query)

    page = request.args.get('page', default=1, type=int)

    movie_per_page = 32
    offset = (page - 1) * movie_per_page

    select_query = f"SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id WHERE movie.series = 2 LIMIT {offset}, {movie_per_page}"
    movies = execute_query(select_query)
    movie_count = len(movies)

    total_page = movie_count // movie_per_page + 1

    pagination = Pagination(page=page, per_page=movie_per_page, total=movie_count, css_framework='bootstrap4')

    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE publish_status.name = 'Sắp chiếu' ORDER BY RAND()LIMIT 5"
    upcomings = execute_query(select_query)
    
    return render_template('phimchieurap.html',categories=categories,nations=nations,page=page,total_page=total_page,movies=movies,upcomings=upcomings,pagination=pagination)


@app.route('/phim-moi', methods=['GET'])
def newmovie():
    select_query = "SELECT id,name FROM category"
    categories = execute_query(select_query)
    select_query = "SELECT id,name FROM nation"
    nations = execute_query(select_query)

    page = request.args.get('page', default=1, type=int)

    movie_per_page = 32
    offset = (page - 1) * movie_per_page

    select_query = f"SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id ORDER BY movie.created_at DESC LIMIT {offset}, {movie_per_page}"
    movies = execute_query(select_query)
    movie_count = len(movies)

    total_page = movie_count // movie_per_page + 1

    pagination = Pagination(page=page, per_page=movie_per_page, total=movie_count, css_framework='bootstrap4')

    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE publish_status.name = 'Sắp chiếu' ORDER BY RAND()LIMIT 5"
    upcomings = execute_query(select_query)
    
    return render_template('phimmoi.html',categories=categories,nations=nations,page=page,total_page=total_page,movies=movies,upcomings=upcomings,pagination=pagination)

@app.route('/phim-bo', methods=['GET'])
def seriesmovie():
    select_query = "SELECT id,name FROM category"
    categories = execute_query(select_query)
    select_query = "SELECT id,name FROM nation"
    nations = execute_query(select_query)

    page = request.args.get('page', default=1, type=int)

    movie_per_page = 32
    offset = (page - 1) * movie_per_page

    select_query = f"WITH ranked_data AS ( SELECT a.*,ROW_NUMBER() OVER (PARTITION BY a.series ORDER BY a.created_at) AS row_num FROM (SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name,  'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,movie.series,movie.created_at FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN  publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id WHERE movie.series NOT IN (1, 2) ORDER BY movie.created_at DESC) a ) SELECT * FROM ranked_data WHERE row_num = 1 LIMIT {offset}, {movie_per_page}"
    movies = execute_query(select_query)
    movie_count = len(movies)

    total_page = movie_count // movie_per_page + 1

    pagination = Pagination(page=page, per_page=movie_per_page, total=movie_count, css_framework='bootstrap4')

    select_query = "SELECT movie.id,movie.name_vn,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.thumbnail,COALESCE(nation.name, 'DefaultValue') AS nation FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN nation ON movie.nation = nation.id WHERE publish_status.name = 'Sắp chiếu' ORDER BY RAND()LIMIT 5"
    upcomings = execute_query(select_query)
    
    return render_template('phimbo.html',categories=categories,nations=nations,page=page,total_page=total_page,movies=movies,upcomings=upcomings,pagination=pagination)

def paginate(page, per_page, total_count):
    num_pages = total_count // per_page + (total_count % per_page > 0)
    return {
        'page': page,
        'per_page': per_page,
        'total_count': total_count,
        'num_pages': num_pages
    }

if __name__ == '__main__':
    app.run(port=5001,host='0.0.0.0')
