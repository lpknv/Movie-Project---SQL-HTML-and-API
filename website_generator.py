from pathlib import Path


def serialize_movie(movie):
    title = movie[0]
    year = movie[1].get("year", "")
    poster_image_url = movie[1].get("poster_image_url")

    poster_html = ""
    if poster_image_url and poster_image_url != "N/A":
        poster_html = f'<img class="movie-poster" src="{poster_image_url}">'

    return f"""<li>
    <div class="movie">
        {poster_html}
        <div class="movie-title">{title}</div>
        <div class="movie-year">{year}</div>
    </div>
</li>"""


def movies_serialized(movies):
    return "".join([serialize_movie(movie) for movie in movies.items()])


def output_movies_html_file(template_path, output_path, replacements):
    try:
        template_path = Path(template_path)
        output_path = Path(output_path)

        html = template_path.read_text(encoding="utf-8")

        for key, value in replacements.items():
            html = html.replace(str(key), str(value))

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        return True

    except FileNotFoundError:
        print(f"Template file not found: {template_path}")
    except PermissionError:
        print(f"No permission to read/write: {template_path} or {output_path}")
    except UnicodeDecodeError:
        print(f"Template is not valid UTF-8: {template_path}")
    except OSError as e:
        print(f"OS error while writing HTML: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return False