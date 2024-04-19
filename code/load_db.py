import pandas as pd

def movie_genres(nodes):

    rows = nodes["movie_genres"].apply(lambda x: x.split(","))

    rows = rows.apply(
        lambda x: [
            i.replace("[", "").replace("]", "").replace("'", "").replace(" ", "") for i in x
        ]
    )

    flat_list = [x for xs in rows.to_list() for x in xs]

    movie_genres = pd.Series(flat_list).unique().tolist()

    return movie_genres