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
def __(mo):
    dataset_id = mo.ui.dropdown(
        options=["D4RL/pointmaze/umaze-v2"]
    )
    dataset_id
    return (dataset_id,)


@app.cell(hide_code=True)
def __(dataset_id, minari):
    # Load Dataset, get variables to be inspected
    if dataset_id.value is None:
        dataset = None
        options = []
    else:
        dataset = minari.load_dataset(dataset_id.value, download=True)

        # Returns of all episodes
        _returns = [_ep.rewards for _ep in dataset.iterate_episodes()]
        lengths = [len(_r) for _r in _returns]
        returns = [_r.sum() for _r in _returns]
        

        if dataset_id.value == "D4RL/pointmaze/umaze-v2":
            options = [f"obs_{_i}" for _i in range(4)]
        else:
            options = []
    return dataset, lengths, options, returns


@app.cell(hide_code=True)
def __(mo):
    mo.md("""## Distribution of episode returns and lengths""")
    return


@app.cell(hide_code=True)
def __(alt, dataset, lengths, pl, returns):
    if dataset is None:
        _chart = None
    else:
        _df = pl.DataFrame({
            "Return": returns,
            "Length": lengths,
        })
        _chart = alt.Chart(_df, width=100, height=100).mark_bar().encode(
            alt.X("Return", bin=True),
            y="count()",
        )
        _chart = alt.Chart(_df, width=100, height=100).mark_bar().encode(
            alt.X("Length", bin=True),
            y="count()",
        )
        
    _chart
    return


@app.cell(hide_code=True)
def __(dataset, mo, n_x, n_y, options):
    if dataset is None:
        total_episodes = 0
    else:
        total_episodes = dataset.total_episodes

    ix_episode = mo.ui.slider(start=0, stop=total_episodes)
    ixs_x = mo.ui.multiselect(options=options, max_selections=n_x)
    ixs_y = mo.ui.multiselect(options=options, max_selections=n_y)

    (ix_episode, ixs_x, ixs_y)
    return ix_episode, ixs_x, ixs_y, total_episodes


@app.cell(hide_code=True)
def __(mo):
    mo.md("""## Rewards in the specified episode""")
    return


@app.cell(hide_code=True)
def __(alt, dataset, ix_episode, pl):
    if dataset is None:
        _chart = None
    else:
        _episode = [_ for _ in dataset.iterate_episodes([ix_episode.value])][0]
        _df = pl.DataFrame({
            "t": range(len(_episode.rewards)),
            "Reward": _episode.rewards
        })
        _chart = alt.Chart(
            _df, width=200.0, height=100.0
        ).mark_line().encode(
            x="t", y="Reward"
        )
    _chart
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md("""## Trajectories of the specified episode""")
    return


@app.cell(hide_code=True)
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
