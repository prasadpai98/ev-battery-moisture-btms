import tkinter as tk
from tkinter import ttk


class DashboardGUI:
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Battery Pack Moisture Monitoring ECU")
        
        
        
        self.root.state("zoomed")

        self.root.configure(bg="#ECECEC")

        # ==========================================================
        # Scrollable Canvas
        # ==========================================================

        self.canvas = tk.Canvas(
            self.root,
            bg="#ECECEC",
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(side="right", fill="y")

        self.canvas.pack(side="left", fill="both", expand=True)

        self.main = tk.Frame(
            self.canvas,
            bg="#ECECEC"
        )

        self.canvas.create_window(
            (0, 0),
            window=self.main,
            anchor="nw"
        )
        
        subtitle = tk.Label(
            self.main,
            text="Real-Time Battery Pack Moisture Monitoring and BTMS Controller",
            font=("Arial",11),
            bg="#ECECEC"
        )

        subtitle.pack(pady=(0,10))
        
        self.main.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.bind_all(
            "<MouseWheel>",
            self._on_mousewheel
        )

        title = tk.Label(
            self.main,
            text="BATTERY PACK MOISTURE MONITORING ECU",
            font=("Arial",20,"bold"),
            bg="#ECECEC"
        )

        title.pack(pady=10)
        
        # ==========================================================
        # INPUT FRAME
        # ==========================================================

        self.input_frame = tk.LabelFrame(

            self.main,

            text="INPUTS",

            font=("Arial", 11, "bold"),

            padx=10,

            pady=10

        )

        self.input_frame.pack(

            fill="x",

            pady=5

        )
        
        self.input_label = tk.Label(
            self.input_frame,
            text="Waiting for measurement...",
            font=("Consolas", 11),
            anchor="w",
            justify="left"
        )

        self.input_label.pack(
            anchor="w",
            fill="x"
        )


        # ==========================================================
        # ROW 1
        # ==========================================================

        self.row1 = tk.Frame(

            self.main,

            bg="#ECECEC"

        )

        self.row1.pack(

            fill="x",

            pady=5

        )


        # ==========================================================
        # ROW 2
        # ==========================================================

        self.row2 = tk.Frame(

            self.main,

            bg="#ECECEC"

        )

        self.row2.pack(

            fill="x",

            pady=5

        )


        # ==========================================================
        # OVERALL STATUS
        # ==========================================================

        self.status_frame = tk.LabelFrame(

            self.main,

            text="OVERALL SYSTEM STATUS",

            font=("Arial",11,"bold"),

            padx=10,

            pady=10

        )

        self.status_frame.pack(

            fill="x",

            pady=5

        )
        
        self.status_label = tk.Label(
            self.status_frame,
            text="System Idle",
            font=("Consolas",11,"bold"),
            anchor="w",
            justify="left"
        )

        self.status_label.pack(
            anchor="w",
            fill="x"
        )
        
        # ==========================================================
        # SECTION FRAMES
        # ==========================================================

        self.calibration_frame = tk.LabelFrame(

            self.row1,

            text="CALIBRATION",

            font=("Arial",11,"bold"),

            padx=10,

            pady=10

        )

        self.calibration_frame.pack(

            side="left",

            expand=True,

            fill="both",

            padx=5

        )
        
        self.calibration_label = tk.Label(
            self.calibration_frame,
            text="Waiting...",
            font=("Consolas",11),
            anchor="w",
            justify="left"
        )

        self.calibration_label.pack(
            anchor="w",
            fill="x"
        )


        self.diagnostic_frame = tk.LabelFrame(

            self.row1,

            text="DIAGNOSTICS",

            font=("Arial",11,"bold"),

            padx=10,

            pady=10

        )

        self.diagnostic_frame.pack(

            side="left",

            expand=True,

            fill="both",

            padx=5

        )
        
        self.diagnostic_label = tk.Label(
            self.diagnostic_frame,
            text="Waiting...",
            font=("Consolas",11),
            anchor="w",
            justify="left"
        )

        self.diagnostic_label.pack(
            anchor="w",
            fill="x"
        )


        self.battery_frame = tk.LabelFrame(

            self.row2,

            text="BATTERY ASSESSMENT",

            font=("Arial",11,"bold"),

            padx=10,

            pady=10

        )

        self.battery_frame.pack(

            side="left",

            expand=True,

            fill="both",

            padx=5

        )
        
        self.battery_label = tk.Label(
            self.battery_frame,
            text="Waiting...",
            font=("Consolas",11),
            anchor="w",
            justify="left"
        )

        self.battery_label.pack(
            anchor="w",
            fill="x"
        )


        self.thermal_frame = tk.LabelFrame(

            self.row2,

            text="THERMAL MANAGEMENT",

            font=("Arial",11,"bold"),

            padx=10,

            pady=10

        )

        self.thermal_frame.pack(

            side="left",

            expand=True,

            fill="both",

            padx=5

        )
        
        self.thermal_label = tk.Label(
            self.thermal_frame,
            text="Waiting...",
            font=("Consolas",11),
            anchor="w",
            justify="left"
        )

        self.thermal_label.pack(
            anchor="w",
            fill="x"
        )


        self.pm_frame = tk.LabelFrame(

            self.main,

            text="PREDICTIVE MAINTENANCE",

            font=("Arial",11,"bold"),

            padx=10,

            pady=10

        )

        self.pm_frame.pack(
            fill="both",
            expand=True,
            pady=5
        )
        
        self.pm_label = tk.Label(
            self.pm_frame,
            text="Waiting...",
            font=("Consolas",11),
            anchor="w",
            justify="left"
        )

        self.pm_label.pack(
            anchor="nw",
            fill="both",
            expand=True
        )

    def run(self):

        self.root.mainloop()

    def update_dashboard(
            self,
            calibration,
            diagnostic,
            battery,
            thermal,
            maintenance,
            temperature=None,
            vpp=None):

        # ===========================
        # INPUTS
        # ===========================

        
    
        self.input_label.config(text=f"""
        Measured VPP : {f"{vpp:.3f}" if vpp is not None else "-"} V

        Temperature : {f"{temperature:.1f}" if temperature is not None else "-"} °C

        Estimated Humidity    : {calibration['humidity']} %

        Source                : LTspice
        """)

        # ===========================
        # CALIBRATION
        # ===========================

        self.calibration_label.config(text=f"""
    Estimated Humidity    : {calibration['humidity']} %
    Measurement Valid     : {calibration['valid']}
    """)

        # ===========================
        # DIAGNOSTICS
        # ===========================

        self.diagnostic_label.config(text=f"""
        Status                : {diagnostic['status']}

        DTC                   : {diagnostic['dtc']}

        Severity              : {diagnostic['severity']}

        Confidence            : {diagnostic['diagnostics_confidence']} %
        """)

        diag_status = diagnostic["status"].upper()

        if diag_status == "HEALTHY":
            colour = "#008000"      # Green

        elif diag_status == "WARNING":
            colour = "#FF8C00"      # Orange

        else:
            colour = "#C00000"      # Red

        self.diagnostic_label.config(
            fg=colour,
            font=("Consolas", 11, "bold")
        )

        # ===========================
        # BATTERY
        # ===========================

        battery_text = f"""
        Battery Status        : {battery['battery_status']}

        Risk Score            : {battery['risk_score']:.1f} /100
        Battery Health        : {battery['battery_health']:.1f} %
        Safety Index          : {battery['safety_index']:.1f} %

        Protection Stage      : {battery['protection_stage']}
        Protection            : {battery['protection_description']}

        Charging              : {"ENABLED" if battery['charging_allowed'] else "DISABLED"}

        ----------------------------------------
        PRIMARY CAUSE
        ----------------------------------------
        """
        for cause in battery["root_causes"]:
            battery_text += f"\n• {cause}"
        
        battery_text += f"""

        ----------------------------------------
        RECOMMENDED ACTION
        ----------------------------------------

        {battery['recommended_action']}
        """
        self.battery_label.config(text=battery_text)

        battery_status = battery["battery_status"].upper()

        if battery_status == "NORMAL":
            colour = "#008000"

        elif battery_status in ("MONITOR", "WARNING"):
            colour = "#FF8C00"

        else:
            colour = "#C00000"

        self.battery_label.config(
            fg=colour,
            font=("Consolas", 11, "bold")
        )

        # ===========================
        # THERMAL
        # ===========================

        thermal_text = f"""
        Mode                  : {thermal['mode']}

        Cooling Fan           : {"ON" if thermal['fan'] else "OFF"}

        Heater                : {"ON" if thermal['heater'] else "OFF"}

        Fan Speed             : {thermal['fan_speed']} %

        Target Temperature    : {thermal['target_temperature']} °C

        Predicted Temperature : {thermal['predicted_temperature']} °C
        """

        self.thermal_label.config(text=thermal_text)

        mode = thermal["mode"].upper()

        if mode == "COOLING":
            colour = "#0066CC"      # Blue

        elif mode == "HEATING":
            colour = "#CC5500"      # Orange

        else:
            colour = "#008000"

        self.thermal_label.config(
            fg=colour,
            font=("Consolas", 11, "bold")
        )

        # ===========================
        # PREDICTIVE MAINTENANCE
        # ===========================

        self.pm_label.config(text=f"""
    Sensor Health         : {maintenance['sensor_health']:.2f} %
    Average Health        : {maintenance['average_health']}
    Trend                 : {maintenance['trend']}
    Maintenance           : {maintenance['maintenance']}
    """)
    
        health = maintenance["sensor_health"]

        if health >= 98:
            colour = "#008000"

        elif health >= 95:
            colour = "#FF8C00"

        else:
            colour = "#C00000"

        self.pm_label.config(
            fg=colour,
            font=("Consolas", 11, "bold")
        )

        # ===========================
        # STATUS
        # ===========================

     
        overall = f"""
        System State          : {battery['battery_status']}

        LTspice Interface     : CONNECTED

        Humidity Sensor       : {diagnostic['status']}

        Thermal Mode          : {thermal['mode']}

        Charging              : {"ENABLED" if battery['charging_allowed'] else "DISABLED"}

        Protection Stage      : {battery['protection_stage']}

        Risk Score            : {battery['risk_score']:.1f}/100
        """

        self.status_label.config(
            text=overall,
            font=("Consolas", 11, "bold")
        )
        
        
    
        
if __name__=="__main__":

    gui=DashboardGUI()

    gui.run()