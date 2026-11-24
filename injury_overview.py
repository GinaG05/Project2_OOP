import streamlit as st


def show_injury_overview(injury_templates):
    st.subheader("Injury Overview")

    injuries = st.session_state["injuries"]

    if not injuries:
        st.info("Add an injury in Report Generator to see it here.")
        return

    injury_rows = []

    for injury in injuries:
        row = {
            "ID": injury.id + 1,
            "Injury Type": injury.injury_type,
            "Location": injury.injury_location["region"],
            "Thread": injury.injury_thread,
            "Suture": injury.injury_suture,
            "Internals": (
                ", ".join(injury.internals)
                if injury.internals
                else "None"
            )
        }

        injury_rows.append(row)

    st.caption("Select a row to view that injury's report.")

    injury_table = st.dataframe(
        injury_rows,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="injury_overview_table"
    )

    selected_rows = injury_table.selection.rows

    if selected_rows:
        selected_index = selected_rows[0]

        if selected_index < len(injuries):
            selected_injury_details = injuries[selected_index]

            selected_report = selected_injury_details.build_injury_report(
                injury_templates
            )

            st.code(selected_report, language="html")

    show_data_chart = st.checkbox(
        "Show injury chart",
        key="show_injury_chart"
    )
    if show_data_chart:
        injury_counts = {}
        for injury in injuries:
            current_injury = injury.injury_type

            if current_injury not in injury_counts:
                injury_counts[current_injury] = 1
            else:
                injury_counts[current_injury] += 1
        #Show data chart is checkbox is checked, otherwise don't display it
        chart_data = {
            "Injury Type": list(injury_counts.keys()),
            "Count": list(injury_counts.values())
        }

        st.bar_chart(
            chart_data,
            x="Injury Type",
            y="Count"
        )