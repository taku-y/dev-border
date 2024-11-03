import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import altair as alt
    import polars as pl
    import minari
    return alt, minari, mo, np, pl


@app.cell
def __():
    # The number of columns and rows
    n_x = 4
    n_y = 4
    return n_x, n_y


@app.cell
def __(pl):
    # Returns polars dataframe
    def get_episode_data(dataset, ix_episode):
        episode = [_ for _ in dataset.iterate_episodes([ix_episode])][0]
        obs = (
            pl.DataFrame(episode.observations["observation"])
            .select(pl.all().name.map(lambda col: col.replace("column", "obs")))
        )
        return obs
    return (get_episode_data,)


@app.cell
def __(dataset_id, minari):
    # Load Dataset
    dataset = minari.load_dataset(dataset_id.value, download=True)

    if dataset_id.value == "D4RL/pointmaze/umaze-v2":
        options = [f"obs_{_i}" for _i in range(4)]
    else:
        options = []
    return dataset, options


@app.cell
def __(mo):
    dataset_id = mo.ui.dropdown(
        options=["D4RL/pointmaze/umaze-v2"]
    )
    dataset_id
    return (dataset_id,)


@app.cell(hide_code=True)
def __(dataset, mo, n_x, n_y, options):
    ix_episode = mo.ui.slider(start=0, stop=dataset.total_episodes)
    ixs_x = mo.ui.multiselect(options=options, max_selections=n_x)
    ixs_y = mo.ui.multiselect(options=options, max_selections=n_y)
    (ix_episode, ixs_x, ixs_y)
    return ix_episode, ixs_x, ixs_y


@app.cell
def __(alt, dataset, get_episode_data, ix_episode, ixs_x, ixs_y):
    df = get_episode_data(dataset, ix_episode.value)

    alt.Chart(df).mark_circle().encode(
        alt.X(alt.repeat("column"), type='quantitative'),
        alt.Y(alt.repeat("row"), type='quantitative'),
        color='Origin:N'
    ).properties(
        width=150,
        height=150
    ).repeat(
        row=ixs_y.value,
        column=ixs_x.value
    )
    return (df,)


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
