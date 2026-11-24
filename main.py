import json
import streamlit as st
from requests import options
from Injury import Injury
from skeleton_picker import pick_injury_location
from medical_chat import show_medical_chat
from injury_overview import show_injury_overview


with open("internal_damage_templates.json", "r", encoding="utf-8") as file:
    templates = json.load(file)

with open("injury_templates.json", "r", encoding="utf-8") as file:
    injury_templates = json.load(file)


##############################
#Session State Initialization#
##############################

if "injuries" not in st.session_state:
    st.session_state["injuries"] = []

if "thread_selection" not in st.session_state:
    st.session_state["thread_selection"] = None

if st.session_state.pop("reset_injury_inputs", False):
    st.session_state["injury_input"] = None
    st.session_state["internals_input"] = []
    st.session_state["suture_input"] = None

if "id_counter" not in st.session_state:
    st.session_state["id_counter"] = 0


######################
#####Sidebar Work#####
######################

if "section" not in st.session_state:
    st.session_state["section"] = "Report Generator"

# Keeps report inputs when navigating to other sections.
report_input_keys = [
    "diagnosis_input",
    "injury_input",
    "internals_input",
    "suture_input",
    "post_treatment",
    "pain_scale",
    "skeleton_view",
]

for key in report_input_keys:
    if key in st.session_state:
        st.session_state[key] = st.session_state[key]


def change_section(section_name):
    st.session_state["section"] = section_name


with st.sidebar:
    st.subheader("Navigation")

    st.button(
        "Report Generator",
        use_container_width=True,
        on_click=change_section,
        args=("Report Generator",)
    )

    if st.session_state["section"] == "Report Generator":
        with st.expander("Report sections", expanded=False):
            st.markdown("[Pre-Treatment](#pre-treatment)")
            st.markdown("[Treatment](#treatment)")
            st.markdown("[Post-Treatment](#post-treatment)")

    st.button(
        "Injury Overview",
        use_container_width=True,
        on_click=change_section,
        args=("Injury Overview",)
    )

    st.button(
        "Medical Q&A",
        use_container_width=True,
        on_click=change_section,
        args=("Medical Q&A",)
    )

# Display the selected section in the main page, then stop this run.
if st.session_state["section"] == "Injury Overview":
    show_injury_overview(injury_templates)
    st.stop()

elif st.session_state["section"] == "Medical Q&A":
    st.subheader("Medical Q&A")
    show_medical_chat()
    st.stop()


##########################################
##########Diagnosis/Pre-Treatment#########
##########################################

st.subheader('Diagnosis', text_alignment="center", divider=True, anchor="pre-treatment")

diagnosis = st.text_area(
    "Diagnosis:",
    label_visibility="collapsed",
    height="content",
    key="diagnosis_input"
)

diagnosis_html = (
    "\n".join(
        f"• {line.strip()}<br>"
        for line in diagnosis.splitlines()
        if line.strip()
    )
    if diagnosis.strip()
    else ""
)


######################################
#####Treatment & Injury Selection#####
######################################

st.subheader(
    "Treatment & Injury Selection",
    text_alignment="center",
    divider=True,
    anchor="treatment"
)

# Injury Selection using selectbox
st.markdown("Select an Injury:")

selected_injury = st.selectbox(
    "Injury:",
    options=injury_templates.keys(),
    index=None,
    label_visibility="collapsed",
    key="injury_input"
)

# Injury Location selection using interactive map/image coords
st.markdown("Select an Injury Location:")

injury_location = pick_injury_location()

if injury_location is None:
    st.caption("Click the skeleton to select an injury location.")
elif injury_location.get("region"):
    st.info(
        f"Selected location: {injury_location['region']} "
        f"({injury_location['view']} view)"
    )
else:
    st.warning("Please click a recognized body region on the skeleton.")

# Internal Damage Selection for current injury
st.markdown(
    f"Select the internal damages present in the "
    f"{selected_injury if selected_injury else 'injury'}:"
)

selected_internals = st.multiselect(
    "Internals:",
    options=templates.keys(),
    placeholder=None,
    label_visibility="collapsed",
    key="internals_input"
)

# Thread Selection
st.markdown(
    f"Please select the type of thread used to close the "
    f"{selected_injury if selected_injury else 'injury'}:"
)

type_of_thread_catgut, type_of_thread_silk = st.columns(2)

with type_of_thread_catgut:
    if type_of_thread_catgut.button(
        "Catgut",
        use_container_width=True,
        key="type_of_thread_catgut"
    ):
        st.session_state["thread_selection"] = "Catgut"

with type_of_thread_silk:
    if type_of_thread_silk.button(
        "Silk",
        use_container_width=True,
        key="type_of_thread_silk"
    ):
        st.session_state["thread_selection"] = "Silk"

if st.session_state["thread_selection"] is not None:
    st.markdown(
        f":green[{st.session_state['thread_selection']} has been selected.]"
    )

# Suture Selection
st.markdown(
    f"Select a suture to close the "
    f"{selected_injury if selected_injury else 'injury'}:"
)

suture_select = st.selectbox(
    "Sutures:",
    [
        "Interrupted Suture",
        "Interrupted Looping Suture",
        "Figure of 8 Interrupted Suture",
        "Continuous Suture",
        "Vertical Mattress Suture",
        "Horizontal Mattress Suture",
        "Five Point Suture",
        "Subcutaneous Suture",
        "Purse String Suture",
    ],
    index=None,
    label_visibility="collapsed",
    key="suture_input"
)


# Add Injury Button
if st.button(f":blue[Add Injury]"):
    if (
        selected_injury is None
        or injury_location is None
        or injury_location.get("region") is None
    ):
        st.warning(
            "Please select an injury and click a recognized body region."
        )

    elif (
        st.session_state["thread_selection"] is None
        or suture_select is None
    ):
        st.warning("Please select the thread & suture to close the injury")

    else:
        new_injury = Injury(
            selected_injury,
            injury_location,
            st.session_state["id_counter"]
        )

        for internals in selected_internals:
            new_injury.add_internals(internals, templates)

        new_injury.injury_closure(
            st.session_state["thread_selection"],
            suture_select
        )

        st.session_state["injuries"].append(new_injury)
        st.session_state["id_counter"] += 1
        st.session_state["injury_success"] = (
            f"{selected_injury} has been added!"
        )

        st.session_state["skeleton_location"] = None
        st.session_state["thread_selection"] = None
        st.session_state["reset_injury_inputs"] = True

        st.rerun()


# Confirm the addition of the injury to the user
message = st.session_state.pop("injury_success", None)

if message:
    st.success(message)

removal_message = st.session_state.pop("injury_remove_success", None)

if removal_message:
    st.success(removal_message)


# Display current injuries
injury_reports = []
injury_names = []

for injury in st.session_state["injuries"]:
    injury_names.append(injury.injury_type)

    injury_report = injury.build_injury_report(injury_templates)
    injury_reports.append(injury_report)

if injury_names:
    st.markdown(
        f":blue[Current injuries: {', '.join(injury_names)}]")

#####Continue#####
if st.session_state["injuries"]:
    injury_to_remove = st.selectbox(
        "Select an injury to remove:",
        options=st.session_state["injuries"],
        index=None,
        format_func=lambda injury: (
            f"#{injury.id + 1} — {injury.injury_type} — "
            f"{injury.injury_location['region']}"
        ),
    )

    if st.button("Remove selected injury"):
        if injury_to_remove is None:
            st.warning("Please select an injury to remove.")

        else:
            remaining_injuries = []

            for injury in st.session_state["injuries"]:
                if injury.id != injury_to_remove.id:
                    remaining_injuries.append(injury)

            st.session_state["injuries"] = remaining_injuries
            st.session_state["injury_remove_success"] = (
                f"{injury_to_remove.injury_type} has been removed!"
            )

            st.rerun()


#############################
#########Post-Treatment######
#############################

st.subheader("Post-Treatment", divider=True, anchor="post-treatment")

post_treatment = st.text_area(
    "Post-Treatment",
    height="content",
    label_visibility="collapsed",
    key="post_treatment"
)

post_treatment_html = (
    "\n".join(
        f"• {line.strip()}<br>"
        for line in post_treatment.splitlines()
        if line.strip()
    )
)

pain_scale = st.number_input(
    "Pain Scale",
    value = None,
    min_value=0,
    max_value=10,
    step=1,
    placeholder = "Enter a pain scale from 0–10",
    key="pain_scale"
)
if pain_scale is not None:
    st.markdown(f":green[Number {pain_scale} has been selected.]")


pain_scale_print = f"• Pain Scale {pain_scale}/10; See 'PRESCRIPTIONS' for further information. <br>  \n"
general_pt_notes = (f"• PT advised of signs of infection and how to take care of the wound. <br>  \n"
                     "• PT advised to return to the office for any questions or concerns, if needed. <br>  \n")


##############################
########Final Printing########
##############################

pre_treatment_header = "<u><b>Summary:</b></u><br>"
treatment_header = "<u><b>Treatment:</b></u><br>"
post_injury_header = "<u><b>Aftercare:</b></u><br>"

if "generated_report_text" not in st.session_state:
    st.session_state["generated_report_text"] = None

if st.button(":blue[Generate Report]", key="generate_report"):
    if injury_reports and post_treatment and pain_scale:
        section_separator = "<br>\n\n"
        combined_report = "\n<br>\n".join(injury_reports)
        full_report = (
                pre_treatment_header + "\n" + diagnosis_html + section_separator + treatment_header + "\n" + combined_report + section_separator + post_injury_header + "\n" + post_treatment_html + "\n" + pain_scale_print + general_pt_notes
        )

        st.session_state["generated_report_text"] = full_report

    else:
        st.session_state["generated_report_text"] = None
        st.warning(
            "Please make sure you have filled all main sections, "
            "or if pre-treatment does not need to be filled, "
            "treatment & post_treatment"
        )

if st.session_state["generated_report_text"] is not None:
    with st.container(
            border=True,
            width="content",
            height="content",
            horizontal=True
    ):
        st.code(
            st.session_state["generated_report_text"],
            language="html"
        )
def reset_all():
    st.session_state["injuries"] = []
    st.session_state["id_counter"] = 0
    st.session_state["generated_report_text"] = None

    st.session_state["diagnosis_input"] = ""
    st.session_state["injury_input"] = None
    st.session_state["internals_input"] = []
    st.session_state["suture_input"] = None
    st.session_state["thread_selection"] = None
    st.session_state["skeleton_location"] = None
    st.session_state["skeleton_view"] = "Front"
    st.session_state["post_treatment"] = ""
    st.session_state["pain_scale"] = 0

    st.session_state.pop("injury_success", None)
    st.session_state.pop("injury_remove_success", None)
    st.session_state.pop("reset_injury_inputs", None)


st.button(
    f":red[Reset all]",
    key="reset_all_button",
    on_click=reset_all
)