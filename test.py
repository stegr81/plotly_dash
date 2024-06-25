def date_format(x):
    return dt.strptime(x, "%m/%d/%Y").date()


def time_format(x):
    return dt.strptime(x, "%H:%M:%S").time()


def create_blank_map():
    fig = px.scatter_mapbox(
        pd.DataFrame({"lat": [], "lon": []}),
        lat="lat",
        lon="lon",
        mapbox_style="carto-darkmatter",
        zoom=1,
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=10), paper_bgcolor="#1E1E1E")
    return fig


def create_map(df):
    max_range = (
        max(max(df["Lat"]) - min(df["Lat"]), max(df["Lon"]) - min(df["Lon"])) * 111
    )
    zoom = 13.5 - np.log(max_range)
    fig = px.scatter_mapbox(
        df, lat=df["Lat"], lon=df["Lon"], mapbox_style="carto-darkmatter", zoom=zoom
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=10), paper_bgcolor="#1E1E1E")
    return fig


def create_blank_chart():
    fig = px.bar().add_annotation(x=10, y=10, text="No Data To Display")
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=10),
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#323130",
        showlegend=False,
        font=dict(color="white"),
    )
    return fig


def create_chart(df):
    fig = px.bar(df["Date"].value_counts())
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=10),
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#323130",
        showlegend=False,
        font=dict(color="white"),
    )
    return fig


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "** GEO RENDERER"
server = app.server


# Plotly mapbox public token
# mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

# Dictionary of important locations in New York


# Initialize data frame
# df = pd.read_csv('uber-raw-data-apr14.csv')
# df[['Date','Time']] = df['Date/Time'].str.split(' ', expand=True)
# df['Date'] = df['Date'].apply(date_format)
# df['Time'] = df['Time'].apply(time_format)

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Div(
                            className="div-for-side-by-side",
                            children=[
                                html.Img(
                                    className="logo",
                                    src=app.get_asset_url("dash-logo-new.png"),
                                ),
                                html.H2("## GEO RENDERER"),
                            ],
                        ),
                        html.Br(),
                        dcc.Upload(
                            id="upload-data",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select FDI File")]
                            ),
                            style={
                                "width": "100%",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "7px",
                                "textAlign": "center",
                                "margin": "5px",
                            },
                            # Allow multiple files to be uploaded
                            multiple=False,
                        ),
                        html.Div(
                            className="fdi_details",
                            id="fdi-output",
                            children=["Once loaded, your FDIs will be shown here."],
                        ),
                        html.P("""Set refresh parameters on initial run:"""),
                        html.Div(
                            className="div-for-side-by-side",
                            children=[
                                dcc.Dropdown(
                                    id="generate-df-delta",
                                    options=[
                                        {
                                            "label": str(n),
                                            "value": str(n),
                                        }
                                        for n in range(1, 25, 1)
                                    ],
                                    multi=False,
                                    maxHeight=120,
                                    placeholder="Time delta for dataframe (hrs)",
                                    style={
                                        "width": "275px",
                                    },
                                ),
                                html.Button(
                                    "Generate Dataframe",
                                    className="button",
                                    id="generate-df-button",
                                    n_clicks=0,
                                ),
                            ],
                        ),
                        html.Div(
                            className="div-for-side-by-side",
                            children=[
                                dcc.Dropdown(
                                    id="refresh-frequency",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in range(5, 65, 5)
                                    ],
                                    placeholder="Set frequency of refresh (mins)",
                                    style={
                                        "width": "275px",
                                    },
                                ),
                                dcc.Checklist(
                                    options=["Auto Refresh"],
                                    value=[],
                                    id="refresh-check",
                                ),
                            ],
                        ),
                        dcc.Dropdown(
                            id="refresh-df-delta",
                            options=[{"label": i, "value": i} for i in range(5, 65, 5)],
                            placeholder="Time delta for auto refresh (hrs)",
                            style={
                                "width": "275px",
                            },
                        ),
                        html.P(
                            """
                            Click a GEO point to display report details:
                            """
                        ),
                        # dcc.Slider(0, len(df['Date'].unique()), 1,
                        #            value=len(df['Date'].unique()),
                        #            id='my-slider'
                        # ),
                        # html.P(id="date-value", children="test"),
                        html.Div(className="div-for-text-display", id="my-output"),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="time-selector",
                                            options=["activity types taken from DF"],
                                            placeholder="Select graph display preference (default activity type)",  # this will be an option to limit by time (options 24 hr, 12 hr...10mins etc)
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Br(),
                        dcc.Markdown(
                            className="contact-details",
                            children=[
                                """
                                            For assistance contact ### Data Science, ##### - ds@email.com
                                        """,
                                """
                                            Main POC ###############
                                        """,
                            ],
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph", figure=create_blank_map()),
                        # html.Div(
                        #     className="text-padding",
                        #     children=[
                        #         "Select any of the bars on the histogram to section data by time."
                        #     ],
                        # ),
                        dcc.Graph(id="histogram", figure=create_blank_chart()),
                    ],
                ),
            ],
        ),
    ]
)


# output details of points when clicked
def parse_content(contents):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    fdi_list = decoded.decode("utf-8").split(",")
    print(fdi_list)
    return fdi_list


@app.callback(
    Output(component_id="fdi-output", component_property="children"),
    Input(component_id="upload-data", component_property="contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
    prevent_initial_call=True,
)
def handle_upload(
    list_of_contents, list_of_names, list_of_dates
):  # needs some error handling
    global fdi_list
    fdi_list = parse_content(list_of_contents)
    fdi_string = ", ".join(fdi_list)
    return f"Your loaded FDIs are {fdi_string}"


@app.callback(
    [
        Output(
            component_id="map-graph", component_property="figure", allow_duplicate=True
        ),
        Output(component_id="histogram", component_property="figure"),
        # and chart
    ],
    [
        # Input(component_id='generate-df-delta', component_property='clickData'),
        Input(component_id="generate-df-button", component_property="n_clicks")
    ],
    prevent_initial_call=True,
)
def create_df(n_clicks):
    # here will be the API in the live version.
    # this will need to handle the time inputs from the drop downs
    # and receive the data from the drag and drop
    df = pd.read_csv(
        "uber-raw-data-apr14.csv"
    )  # changing the formatting to the new version in the live app
    df[["Date", "Time"]] = df["Date/Time"].str.split(" ", expand=True)
    df["Date"] = df["Date"].apply(date_format)
    df["Time"] = df["Time"].apply(time_format)
    df = df.sample(n=1000)
    map_fig = create_map(df)
    map_fig.show()
    chart_fig = create_chart(df)
    return map_fig, chart_fig


############# take the callbacks above this line for live version #####################


@app.callback(
    Output(component_id="my-output", component_property="children"),
    Input(component_id="map-graph", component_property="clickData"),
    prevent_initial_call=True,
)
def update_output_div(clickData):
    return f"{clickData['points'][0]['lat']},{clickData['points'][0]['lon']}"
    # return f"{clickData}"


# update map based on time selection
@app.callback(
    Output(component_id="map-graph", component_property="figure", allow_duplicate=True),
    [
        Input(component_id="time-selector", component_property="value"),
        Input(component_id="histogram", component_property="clickData"),
    ],
    prevent_initial_call=True,
)
def filter_map(time_picked, selected_data):
    if time_picked:
        temp_df = df[df["Date"] == dt.strptime(time_picked, "%Y-%m-%d").date()]
        max_range = (
            max(
                max(temp_df["Lat"]) - min(temp_df["Lat"]),
                max(temp_df["Lon"]) - min(temp_df["Lon"]),
            )
            * 111
        )
        zoom = 13.5 - np.log(max_range)
        # print(temp_df)
        fig = px.scatter_mapbox(
            temp_df,
            lat=temp_df["Lat"],
            lon=temp_df["Lon"],
            mapbox_style="carto-darkmatter",
            zoom=zoom,
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=10), paper_bgcolor="#1E1E1E")
        return fig
    if selected_data:
        # print(selected_data['points'][0]['label'])
        temp_df = df[
            df["Date"]
            == dt.strptime(selected_data["points"][0]["label"], "%Y-%m-%d").date()
        ]
        max_range = (
            max(
                max(temp_df["Lat"]) - min(temp_df["Lat"]),
                max(temp_df["Lon"]) - min(temp_df["Lon"]),
            )
            * 111
        )
        zoom = 13.5 - np.log(max_range)
        # print(temp_df)
        fig = px.scatter_mapbox(
            temp_df,
            lat=temp_df["Lat"],
            lon=temp_df["Lon"],
            mapbox_style="carto-darkmatter",
            zoom=zoom,
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=10), paper_bgcolor="#1E1E1E")
        return fig


if __name__ == "__main__":
    app.run_server(jupyter_mode="external", debug=True)
