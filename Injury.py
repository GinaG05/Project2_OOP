class Injury:
    def __init__(self, injury_type, injury_location, injury_id):
        self.injury_type = injury_type
        self.injury_location = injury_location
        self.internals = {}
        self.injury_thread = ""
        self.injury_suture = ""
        self.id = injury_id


    def add_internals(self, internal_type, templates):
        internal_priority = templates[internal_type]["priority"]
        internal_txt_data = templates[internal_type]["text"].copy()

        self.internals[internal_type] = {
            "priority": internal_priority,
            "text": internal_txt_data
        }

    def delete_internal(self, internal_type):
        self.internals.pop(internal_type, None)

    def build_internals_report(self):
        ordered = sorted(
            self.internals.values(),
            key=lambda internal: internal["priority"])

        report_txt = []
        for internal in ordered:
            report_txt.extend(internal["text"])

        return "<br>  \n".join(report_txt)

    def injury_closure(self, injury_thread, injury_suture):
        self.injury_thread = injury_thread
        self.injury_suture = injury_suture

    def build_injury_report(self, injury_templates):
        injury_type = self.injury_type
        template = injury_templates[injury_type]
        injury_init_obs = template["initial_obs"]
        injury_if_vascular = template["if_vascular"]
        injury_close = template["close"]


        if "Arterial (Nicked)" in self.internals or "Arterial (Severed/Jagged)" in self.internals:
            bleeding_observation = "bright red (arterial) blood observed."
            vessel = "artery"
        elif "Venous (Nicked)" in self.internals or "Venous (Severed/Jagged)" in self.internals:
            bleeding_observation = "dark red (venous) blood observed."
            vessel = "vein"
        else:
            bleeding_observation = "none observed."
            vessel = None

        internal_damage = ", ".join(self.internals) if self.internals else "none"
        final_report = []

        final_report.append(f"{injury_type} - {self.injury_location['region']}")

        for line in injury_init_obs:
            formatted_line = line.format(
                bleeding_observation=bleeding_observation,
                internal_damage=internal_damage
            )
            final_report.append(formatted_line)

        if vessel is not None:
            for line in injury_if_vascular:
                formatted_line = line.format(vessel=vessel)
                final_report.append(formatted_line)

        if "remove_bullet" in template:
            final_report.extend(template["remove_bullet"])

        internal_report = self.build_internals_report()
        if internal_report:
            final_report.append(internal_report)

        for line in injury_close:
            formatted_line = line.format(
                injury_thread=self.injury_thread,
                injury_suture=self.injury_suture
            )
            final_report.append(formatted_line)

        return "<br>  \n".join(final_report) + "<br>"


