def load_template(file_path):
  """ Loads a template html file as a string"""
  with open(file_path, "r") as template:
    return template.read()

def write_html(file_path, content):
    """ Write the html file with specified content """
    with open(file_path, "w") as file:
        file.write(content)

def serialize_movie(movie) -> str:
    """ Serialize an animal object """
    output_string = f''
    output_string += f'        <li>\n'
    output_string += f'            <div class="movie">\n'
    output_string += f'                <img class="movie-poster"\n'
    output_string += f'                     src="{movie["poster_url"]}" alt="{movie["title"]}">\n'
    output_string += f'                <div class="movie-title">{movie["title"]}</div>\n'
    output_string += f'                <div class="movie-year">{movie["year"]}</div>\n'
    output_string += f'            </div>\n'
    output_string += f'        </li>\n'
    return output_string
