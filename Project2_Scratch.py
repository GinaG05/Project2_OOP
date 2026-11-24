from email.policy import default
from operator import truediv

import streamlit as st

#################################
#########Tab Declaration#########
#################################
tab1, tab2, tab3, tab4 = st.tabs(["Main", "Pre-Treatment", "Treatment", "Post-Treatment"], key="tabs", on_change="rerun")

def confirm_vitals():
    st.session_state["vitals_updated"] = True
def confirm_consciousness():
    st.session_state["consciousness_updated"] = True

def go_to_pre_treatment():
    st.session_state["tabs"] = "Pre-Treatment"
def go_to_post_treatment_1():
    st.session_state["tabs"] = "Post-Treatment"
    for injury_select in st.session_state["internal_indexes_for_final_report"]:
        if injury_select == "Muscle (Torn)":
            st.session_state["internal_final"] += st.session_state["internals_MT_final"]
        elif injury_select == "Muscle (Severed/Jagged)":
            st.session_state["internal_final"] += st.session_state["internals_MS_final"]
        elif injury_select == "Venous (Severed/Jagged)":
            st.session_state["internal_final"] += st.session_state["internals_VS_final"]
        elif injury_select == "Venous (Nicked)":
            st.session_state["internal_final"] += st.session_state["internals_VN_final"]
        elif injury_select == "Arterial (Severed/Jagged)":
            st.session_state["internal_final"] += st.session_state["internals_AS_final"]
        elif injury_select == "Arterial (Nicked)":
            st.session_state["internal_final"] += st.session_state["internals_AN_final"]

def go_to_treatment():
    st.session_state["tabs"] = "Treatment"
def go_to_main():
    st.session_state["tabs"] = "Main"




#===============================
#Main Page
#===============================

with tab1:
    st.title("Medical Report Generator")
    st.write("This app allows you to generate Medical Reports for general injuries you encounter in roleplay on a daily basis.")

#===============================
#Pre-Treatment Page
#===============================

with tab2:
    if "has_pre_treatment" not in st.session_state:
        st.session_state["has_pre_treatment"] = False
    if "pre_treatment_final_report" not in st.session_state:
        st.session_state["pre_treatment_final_report"] = ""

    st.markdown("Would you like to generate the pre-treatment portion of the report?")
    pre_treatment_yes, pre_treatment_no = st.columns(2)
    with pre_treatment_yes:
        if pre_treatment_yes.button(f":green[Yes]", use_container_width=True, key="pre_treatment_yes"):
            st.session_state["has_pre_treatment"] = True
    with pre_treatment_no:
        if pre_treatment_no.button(f":red[No]", use_container_width=True, key="pre_treatment_no"):
            st.session_state["has_pre_treatment"] = False

    vitals = ""
    consciousness = ""
    numbYes = ""
    if st.session_state["has_pre_treatment"]:
        vitals = st.text_area("Please describe the patient's vitals below:", key="input_vitals",  on_change=confirm_vitals)

        if st.session_state.pop("vitals_updated", False):
            st.success("Vitals input has been recorded.")

        consciousness = st.text_area("Please write if the patient was conscious, or unconscious, and any additional information below:", key = "input_consciousness", on_change=confirm_consciousness)

        if st.session_state.pop("confirm_consciousness", False):
            st.success("Vitals input has been recorded.")

        numbing = st.selectbox("Was numbing administered?", ["Clove Oil", "Cocaine Paste", "None Applied"])
        if numbing == "Clove Oil":
            numbYes = "• Clove oil applied around the wound in order to numb the area.<br>"
        elif numbing == "Cocaine Paste":
            numbYes = "• Cocaine Paste applied around the wound in order to numb the area.<br>"
        else:
            pass

    pre_treatment_final =  (
        "<u><b>Pre-Treatment:</b></u>  \n"
        "<br>  \n"
        f"• Vitals Checked, {vitals} <br>  \n"
        f"• Consciousness: {consciousness} <br>  \n"
        f" {numbYes} <br>  \n"
    )
    st.session_state["pre_treatment_final_report"] = pre_treatment_final


###############################################################
##################End of Pre-Treatment#########################
###############################################################

#===============================
#Treatment Page
#===============================

with tab3:
    ###############################################################
    ###############Session State Variable Declarations#############
    ###############################################################
    if "internals_index" not in st.session_state: #Starts internals "list" selections at index 0, to be incremented by a button called Next
        st.session_state["internals_index"] = 0
    if "type_of_thread" not in st.session_state:
        st.session_state["type_of_thread"] = ""
    if "type_of_thread_for_muscle_used" not in st.session_state:
        st.session_state["type_of_thread_for_muscle_used"] = ""
    if "internal_final" not in st.session_state:
        st.session_state["internal_final"] = ""
    if "internals_copy" not in st.session_state:
        st.session_state["internals_copy"] = ""
    if "internals_MT_final" not in st.session_state:
        st.session_state["internals_MT_final"] = ""
    if "internals_MS_final" not in st.session_state:
        st.session_state["internals_MS_final"] = ""
    if "internals_VS_final" not in st.session_state:
        st.session_state["internals_VS_final"] = ""
    if "internals_VN_final" not in st.session_state:
        st.session_state["internals_VN_final"] = ""
    if "internals_AS_final" not in st.session_state:
        st.session_state["internals_AS_final"] = ""
    if "internals_AN_final" not in st.session_state:
        st.session_state["internals_AN_final"] = ""
    if "internal_indexes_for_final_report" not in st.session_state:
        st.session_state["internal_indexes_for_final_report"] = ""
    if "final_injuries" not in st.session_state:
        st.session_state["final_injuries"] = ""

    ###############################################################
    ##################Variable Declaration#########################
    ###############################################################
    internal_MT = ""
    internal_MS = ""
    internal_VS = ""
    internal_VN = ""
    internal_AS = ""
    internal_AN = ""
    st.markdown("*To continue, please select an injury below:*")
    injuries = st.selectbox("Injury Selection",
                            ["Gunshot Wound (Lodged)", "Gunshot Wound (T&T)", "Animal Punctures/Laceration"], index = None)  # To be continued

#Add session state for type_of_thread(s)
    st.markdown(f"Please select the type of thread used to close the {injuries}")
    type_of_thread_catgut, type_of_thread_silk = st.columns(2)
    with type_of_thread_catgut:
        if type_of_thread_catgut.button("Catgut", use_container_width=True, key="type_of_thread_catgut"):
           # st.session_state["has_suture_chosen"] = True
            st.session_state["type_of_thread"] = "Catgut"
            st.markdown(f":green[Catgut has been selected.]")
    with type_of_thread_silk:
        if type_of_thread_silk.button("Silk",use_container_width=True, key="type_of_thread_silk"):
            #st.session_state["has_suture_chosen"] = True
            st.session_state["type_of_thread"] = "Silk"
            st.markdown(f":green[Silk has been selected.]")
    type_of_suture = st.selectbox("Please select the type of suture used to close the wound:", ["Interrupted Suture", "Interrupted Looping Suture", "Figure of 8 Interrupted Suture", "Continuous Suture", "Vertical Mattress Suture", "Horizontal Mattress Suture", "Five Point Suture", "Subcutaneous Suture", "Purse String Suture"], key = "type_of_suture", index = None)

    internals = st.multiselect(f"Please select the internal damage sustained to the {injuries}. If there was no internal damage, leave the follow selection blank.", ["Muscle (Torn)", "Muscle (Severed/Jagged)", "Venous (Severed/Jagged)", "Venous (Nicked)", "Arterial (Severed/Jagged)", "Arterial (Nicked)"], placeholder = "None")



    if st.session_state["internals_copy"] != internals:
        st.session_state["internal_final"] = ""
        for injury in st.session_state["internals_copy"]:
            if injury not in internals:
                if st.session_state["internals_copy"].index(injury) < st.session_state["internals_index"]:
                    st.session_state["internals_index"] -= 1
            if injury in internals:
                if injury == "Muscle (Torn)":
                    st.session_state["internal_final"] += st.session_state["internals_MT_final"]
                if injury == "Muscle (Severed/Jagged)":
                    st.session_state["internal_final"] += st.session_state["internals_MS_final"]
                if injury == "Venous (Severed/Jagged)":
                    st.session_state["internal_final"] += st.session_state["internals_VS_final"]
                if injury == "Venous (Nicked)":
                    st.session_state["internal_final"] += st.session_state["internals_VN_final"]
                if injury == "Arterial (Severed/Jagged)":
                    st.session_state["internal_final"] += st.session_state["internals_AS_final"]
                if injury == "Arterial (Nicked)":
                    st.session_state["internal_final"] += st.session_state["internals_AN_final"]
    st.session_state["internals_copy"] = internals

################################
    #Re-Order Internals List#
################################

    st.session_state["internal_indexes_for_final_report"] = internals.copy()
    if "Arterial (Nicked)" in st.session_state["internal_indexes_for_final_report"]:
        st.session_state["internal_indexes_for_final_report"][st.session_state["internal_indexes_for_final_report"].index("Arterial (Nicked)")], st.session_state["internal_indexes_for_final_report"][0] = st.session_state["internal_indexes_for_final_report"][0], st.session_state["internal_indexes_for_final_report"][st.session_state["internal_indexes_for_final_report"].index("Arterial (Nicked)")]
    elif "Arterial (Severed/Jagged)" in st.session_state["internal_indexes_for_final_report"]:
        injury_index = st.session_state["internal_indexes_for_final_report"].index("Arterial (Severed/Jagged)")
        st.session_state["internal_indexes_for_final_report"][injury_index], st.session_state["internal_indexes_for_final_report"][0] = st.session_state["internal_indexes_for_final_report"][0], st.session_state["internal_indexes_for_final_report"][injury_index]
    elif "Venous (Nicked)" in st.session_state["internal_indexes_for_final_report"]:
        injury_index = st.session_state["internal_indexes_for_final_report"].index("Venous (Nicked)")
        st.session_state["internal_indexes_for_final_report"][injury_index], st.session_state["internal_indexes_for_final_report"][0] = st.session_state["internal_indexes_for_final_report"][0], st.session_state["internal_indexes_for_final_report"][injury_index]
    elif "Venous (Severed/Jagged)" in st.session_state["internal_indexes_for_final_report"]:
        injury_index = st.session_state["internal_indexes_for_final_report"].index("Venous (Severed/Jagged)")
        st.session_state["internal_indexes_for_final_report"][injury_index], st.session_state["internal_indexes_for_final_report"][0] = st.session_state["internal_indexes_for_final_report"][0], st.session_state["internal_indexes_for_final_report"][injury_index]

    message = st.session_state.pop("internal_confirmation", None)
    if message:
        st.success(message)

    if st.session_state["internals_index"] == len(internals):
        with st.container():
            st.button(f":blue[Submit & Go To Post-Treatment]", key="gt_post_treatment", on_click=go_to_post_treatment_1)

    if st.session_state["internals_index"] < len(internals):
        @st.dialog("Internal Injuries:", width = "large", dismissible = True)
        def dialogue_decorator1(internals):
            st.markdown(f"Please select the type of suture used to close the muscle layer for {internals[st.session_state["internals_index"]]}:")
            type_of_suture_for_muscle_used = st.selectbox("Type of Suture Used:", ["Interrupted Suture", "Interrupted Looping Suture",
                                                                       "Figure of 8 Interrupted Suture",
                                                                       "Continuous Suture", "Vertical Mattress Suture",
                                                                       "Horizontal Mattress Suture", "Five Point Suture",
                                                                       "Subcutaneous Suture", "Purse String Suture"], key = f"type_of_suture_for_muscle_used_{st.session_state['internals_index']}")
            # Add session state for type_of_thread_for_muscle_used
            st.markdown("Please select the type of thread used to close the muscle layer:")
            type_of_suture_thread_for_muscle_silk, type_of_suture_thread_for_muscle_catgut = st.columns(2)

            with type_of_suture_thread_for_muscle_silk:
                if st.button("Silk", key = "type_of_thread_used_muscle_silk", use_container_width=True):
                    st.session_state["type_of_thread_for_muscle_used"] = "Silk"
                    st.markdown(f":green[Silk has been selected.]")
            with type_of_suture_thread_for_muscle_catgut:
                if st.button("Catgut", key = "type_of_thread_used_muscle_catgut", use_container_width=True):
                    st.session_state["type_of_thread_for_muscle_used"] = "Catgut"
                    st.markdown(f":green[Catgut has been selected.]")

            if internals[st.session_state["internals_index"]] == "Muscle (Torn)":

                internal_MT = f"• Wound flushed wih saline and inspected for internal damage: muscle (Torn) observed. <br>  \n"\
                              f"• Wound flushed with DCA & Saline. <br>  \n"\
                              f"• A sterile C-hook was threaded with {st.session_state["type_of_thread_for_muscle_used"]} and utilized to suture the muscle with {type_of_suture_for_muscle_used}. Held well. <br>  \n"
                st.session_state["internals_MT_final"] = internal_MT

            if internals[st.session_state["internals_index"]] == "Muscle (Severed/Jagged)":

                internal_MS =   f"• Wound flushed wih saline and inspected for internal damage: muscle (Severed) observed. <br>  \n" \
                                f"• Wound flushed with DCA & Saline. <br>  \n"\
                                f"• A sterile scalpel was utilized to trim the damaged muscle tissue. <br>  \n"\
                                f"• A sterile C-hook was threaded with {st.session_state["type_of_thread_for_muscle_used"]} and utilized to suture the muscle with {type_of_suture_for_muscle_used} <br>.  \n"

                st.session_state["internals_MS_final"] = internal_MS

            if internals[st.session_state["internals_index"]] == "Venous (Severed/Jagged)":
                internal_VS = f"• Severity of the damage to the vein was assessed and observed to be severed/jagged.<br>  \n"\
                              f"• A sterile scalpel was utilized in order to trim the slanted edged of the vein. <br>  \n"\
                              f"• Wound flushed thoroughly with Saline. <br>  \n"\
                              f"• A sterile C-hook was threaded with silk and utilized to suture the vein with an interrupted looping stitch. Held well. <br>  \n"\
                              f"• Hemostats were removed, distally and then proximally, and vein checked for leakage: none present. <br>  \n" \
                              f"• Wound flushed with DCA & Saline. <br>  \n"

                        #f"• Wound was flushed with saline and inspected to have signs of a venous bleed: Dark Red Blood seeping through the wound.<br>\n" \
                        #f"• Sterile hemostats were applied to either side of the damaged vein (proximally, and then distally). <br> \n" \
                st.session_state["internals_VS_final"] = internal_VS

            if internals[st.session_state["internals_index"]] == "Venous (Nicked)":
                internal_VN = f"• Severity of the damage to the vein was assessed and observed to be nicked.<br>\n"\
                              f"• Wound flushed thoroughly with Saline. <br> \n"\
                              f"• A sterile C-hook was threaded with silk and utilized to suture the vein with an interrupted looping stitch. Held well. <br> \n"\
                              f"• Hemostats were removed, distally and then proximally, and vein checked for leakage: none present. <br>\n" \
                              f"• Wound flushed with DCA & Saline. <br> \n"

                #f"• Wound was flushed with saline and inspected to have signs of a venous bleed: Dark Red Blood seeping through the wound.<br>\n" \
                #f"• Sterile hemostats were applied to either side of the damaged vein (proximally, and then distally). <br> \n" \

                st.session_state["internals_VN_final"] = internal_VN

            if internals[st.session_state["internals_index"]] == "Arterial (Severed/Jagged)":
                internal_AS = f"• Severity of the damage to the artery was assessed and observed to be severed/jagged.<br>  \n"\
                              f"• A sterile scalpel was utilized in order to trim the slanted edged of the artery. <br>  \n"\
                              f"• Wound flushed thoroughly with Saline. <br>  \n"\
                              f"• A sterile C-hook was threaded with silk and utilized to suture the artery with an interrupted looping stitch. Held well. <br>  \n"\
                              f"• Hemostats were removed, distally and then proximally, and artery checked for leakage: none present. <br>  \n" \
                              f"• Wound flushed with DCA & Saline. <br>  \n"

                            #f"• Wound was flushed with saline and inspected to have signs of an arterial bleed: Bright Red Blood seeping through the wound.<br>\n" \
                            #f"• Sterile hemostats were applied to either side of the damaged artery (proximally, and then distally). <br> \n" \
                st.session_state["internals_AS_final"] = internal_AS


            if internals[st.session_state["internals_index"]] == "Arterial (Nicked)":
                internal_AN =   f"• Severity of the damage to the artery was assessed and observed to be nicked.<br>  \n" \
                                f"• Wound flushed thoroughly with Saline. <br>  \n" \
                                f"• A sterile C-hook was threaded with silk and utilized to suture the artery with an interrupted looping stitch. Held well. <br>  \n" \
                                f"• Hemostats were removed, distally and then proximally, and artery checked for leakage: none present. <br>  \n" \
                                f"• Wound flushed with DCA & Saline. <br>  \n"

            # f"• Wound was flushed with saline and inspected to have signs of an arterial bleed: Bright Red Blood seeping through the wound.<br>\n" \
            # f"• Sterile hemostats were applied to either side of the damaged artery (proximally, and then distally). <br> \n" \
                st.session_state["internals_AN_final"] = internal_AN


            if st.button("Close & Submit"):
                if st.session_state["internals_index"] < len(internals):
                    current_internal = internals[st.session_state["internals_index"]]

                    st.session_state["internal_confirmation"] = (
                        f"{current_internal} answers have been recorded."
                    )
                    st.session_state["internals_index"] += 1
                    st.session_state["type_of_thread_for_muscle_used"] = ""
                    st.rerun()



        dialogue_decorator1(internals)


    #=========================================
    #Start of Back-End Injury Output Selection
    #=========================================

    GSW_pt1 = ""
    GSW_pt2_for_blood_vessels = ""
    GSW_pt3 = ""
    GSW_pt4 = ""
    GSW_final_holder = ""
    gsw_tnt_final_holder = ""


    if injuries == "Gunshot Wound (Lodged)":
        GSW_pt1 = f"• Wound flushed with saline and inspected for any venous (dark red) or arterial (bright red) blood seeping through the wound: {'arterial blood observed.' if "Arterial (Nicked)" in internals or "Arterial (Severed/Jagged)" in internals else 'venous blood observed.' if "Venous (Nicked)" in internals or "Venous (Severed/Jagged)" in internals else 'none present.'} <br>  \n"
        GSW_final_holder += GSW_pt1

        GSW_pt2_for_blood_vessels = f"• Dil-Iodine applied to the skin around the wound. <br>  \n" \
                                    f"• A sterile scalpel was utilized to make an incision on either side of the wound in order to gain access to the damaged {'artery' if "Arterial (Nicked)" or "Arterial (Severed/Jagged)" in internals else 'vein' if "Venous (Nicked)" or "Venous (Severed/Jagged)" in internals else ''}. <br>  \n"\
                                    f"• Sterile hemostats were applied to either side of the damaged {'artery' if "Arterial (Nicked)" or "Arterial (Severed/Jagged)" in internals else 'vein' if "Venous (Nicked)" or "Venous (Severed/Jagged)" in internals else ''} (proximally, and then distally). <br>  \n" \
                                    f"• Sterile forceps were utilized to remove the bullet, which was successful and came out whole. <br>  \n"\

        if "Arterial (Nicked)" in internals or "Arterial (Severed/Jagged)" in internals:
            GSW_final_holder += GSW_pt2_for_blood_vessels
            GSW_final_holder += st.session_state["internal_final"]
        elif "Venous (Nicked)" in internals or "Venous (Severed/Jagged)" in internals:
            GSW_final_holder += GSW_pt2_for_blood_vessels
            GSW_final_holder += st.session_state["internal_final"]
        elif "Muscle (Torn)" or "Muscle (Severed/Jagged" in internals:
            GSW_pt3 = f"• Sterile forceps were utilized to remove the bullet, which was successful and came out whole. <br>  \n"
            GSW_final_holder += GSW_pt3
            GSW_final_holder += st.session_state["internal_final"]

        GSW_pt4 = f"• C-hook was resterilized and rethreaded with {st.session_state["type_of_thread"]} and a {type_of_suture} pattern was utilized to suture the wound closed. Held well <br>  \n"
        GSW_final_holder += GSW_pt4
        st.session_state["final_injuries"] += GSW_final_holder

    if injuries == "Gunshot Wound (T&T)":
        gsw_tnt_pt1 = f"• Wound flushed with saline and inspected for internal damage: {internals} observed. <br>  \n"
        gsw_tnt_final_holder += gsw_tnt_pt1
        blood_vessels_pt2 = f"• Sterile hemostats were applied to either side of the damaged {'artery' if "Arterial (Nicked)" or "Arterial (Severed/Jagged)" in internals else 'vein' if "Venous (Nicked)" or "Venous (Severed/Jagged)" in internals else ''} (proximally, and then distally). <br>  \n"

        if "Arterial (Nicked)" or "Arterial (Severed/Jagged)" in internals:
            gsw_tnt_final_holder += blood_vessels_pt2
            gsw_tnt_final_holder += st.session_state["internal_final"]
        elif "Venous (Nicked)" in internals or "Venous (Severed/Jagged)" in internals:
            gsw_tnt_final_holder += blood_vessels_pt2
            gsw_tnt_final_holder += st.session_state["internal_final"]
        elif "Muscle (Torn)" or "Muscle (Severed/Jagged" in internals:
            gsw_tnt_final_holder += st.session_state["internal_final"]
        elif "" in internals:
            gsw_tnt_pt5 = (f"• Wound flushed with DCA & Saline. <br>  \n"
                           f"• C-hook was resterilized and rethreaded with {st.session_state["type_of_thread"]} and a {type_of_suture} pattern was utilized to close the EXIT wound. <br>  \n"
                           f"• Wound flushed with DCA & Saline. <br>  \n"
                           f"• C-hook was resterilized and rethreaded with {st.session_state["type_of_thread"]} and a {type_of_suture} pattern was utilized to close the ENTRY wound. <br>  \n"
                           )
            gsw_tnt_final_holder += gsw_tnt_pt5
        st.session_state["final_injuries"] += gsw_tnt_final_holder

    if injuries == "Animal Punctures/Laceration":
        final_animal_injuries = ""

        if "Arterial (Nicked)" or "Arterial (Severed/Jagged)" in internals:
            final_animal_injuries += blood_vessels_pt2
            final_animal_injuries += st.session_state["internal_final"]
        elif "Venous (Nicked)" in internals or "Venous (Severed/Jagged)" in internals:
            final_animal_injuries+= blood_vessels_pt2
            final_animal_injuries += st.session_state["internal_final"]
        elif "Muscle (Torn)" or "Muscle (Severed/Jagged" in internals:
            final_animal_injuries += st.session_state["internal_final"]
        elif "" in internals:
            animal_injuries_pt1 =  f"• A sterile C-hook was threaded with {st.session_state["type_of_thread"]} and a {type_of_suture} pattern was utilized to suture the wound closed. Held well <br>  \n"
            final_animal_injuries += animal_injuries_pt1

        st.session_state["final_injuries"] += final_animal_injuries

with tab4:
    if "has_iv_administered" not in st.session_state:
        st.session_state["has_iv_administered"] = None
    if "final_post_treatment_report" not in st.session_state:
        st.session_state["final_post_treatment_report"] = ""

    post_treatment_final = ""

    general_post_treatment = (f"• Dil-Iodine applied atop sutures. <br>  \n"
                             f"• Herbal Salve applied around the sutures. <br>  \n"
                             f"• Wound wrapped in sterile gauze bandaging. <br>  \n")
    post_treatment_final += general_post_treatment

    pain_scale_value = st.number_input("Enter the Patient's Reported Pain Scale Number", min_value=0, step=1, value=None, placeholder="Type a number...")
    st.markdown(f"The current number recorded is :green[{pain_scale_value}]")

    pain_scale = f"Patient reported a pain scale of {pain_scale_value}/10; See 'Prescriptions' for further information. <br>  \n"
    post_treatment_final += pain_scale

    iv = ""
    st.write("Was an IV administered?")
    iv_yes, iv_no = st.columns(2)
    with iv_yes:
        if iv_yes.button("Yes", use_container_width=True, key="iv_yes_clicked"):
            st.session_state["has_iv_administered"] = True

        if st.session_state["has_iv_administered"] and (
                "Arterial (Nicked)" or "Arterial (Severed/Jagged)" or "Venous (Nicked)" or "Venous (Severed/Jagged)" in
                st.session_state["internal_final"]):

            iv = "• IV Administered once blood vessels injuries were repaired. <br>"  # Add a checker here depending on if there was an arterial/venous bleed

        elif st.session_state["has_iv_administered"] and (injuries != "Arterial Bleed" and injuries != "Venous Bleed"):
            iv = "• IV Administered"

    with iv_no:
        if iv_no.button("No", use_container_width=True, key="iv_no_clicked"):
            st.session_state["has_iv_administered"] = False

    post_treatment_final += iv


    ####################
    #Back to Main
    ####################
    with st.container(border= True, width= "content", height="content"):
        st.markdown(f"{st.session_state["pre_treatment_final_report"], st.session_state["final_injuries"], post_treatment_final}", unsafe_allow_html=False)








