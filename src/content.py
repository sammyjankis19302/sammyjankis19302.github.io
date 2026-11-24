"""Everything the site says lives in this file.

Edit the text here, then run `python3 src/build.py` from the repository root.
Strings are HTML: use &nbsp; between a number and its unit, and <a href="...">...</a> for links.
"""

BASE_URL = "https://sammyjankis19302.github.io/"
UPDATED = "2026-11-25"          # shown in the footer and written to sitemap.xml
UPDATED_TEXT = "November 2026"

NAME = "Akula Uday Kiran"
EMAIL = "sammyjankis19302@gmail.com"
GITHUB = "https://github.com/sammyjankis19302"
LINKEDIN = "https://www.linkedin.com/in/akulaudaykiran19302/"

TITLE = "Akula Uday Kiran – Aerospace engineering, RV College of Engineering"
DESCRIPTION = (
    "Akula Uday Kiran is a final-year aerospace engineering student at RV College of Engineering "
    "(RVCE), Bengaluru, with research internships at CSIR–National Aerospace Laboratories and DRDO's "
    "Advanced Systems Laboratory. Computational fluid dynamics, numerical methods, hypersonic "
    "heating and rocket propulsion, with projects published in full as public repositories."
)

NAV = [("experience", "Experience"), ("projects", "Projects"), ("path", "Four years"),
       ("awards", "Awards"), ("contact", "Contact")]

# ---------------------------------------------------------------- hero
LEDE = (
    "I’m a final-year aerospace engineering student at RV College of Engineering in Bengaluru. "
    "I work on computational fluid dynamics, numerical methods and rocket propulsion, and I trust a "
    "result only once it has survived a check that could have proved it wrong."
)

SPEC = [
    ("Studying", "B.E. Aerospace Engineering, RVCE, 2023–2027"),
    ("CGPA", "9.25 / 10 after six semesters"),
    ("Research", "CSIR–NAL, Bengaluru, 2026<br>DRDO ASL, Hyderabad, 2025"),
    ("Next", "Applying for MS programmes in aerospace engineering, autumn 2027"),
]

FLOW_CAPTION = (
    "Potential flow past a cambered Joukowski aerofoil, computed live in your browser and coloured "
    "by speed, slow in blue and fast in orange. The circulation comes from the Kutta condition, so "
    "the flow leaves the sharp trailing edge smoothly. The flow is inviscid, so this aerofoil never stalls."
)

# ---------------------------------------------------------------- experience
EXPERIENCE = [
    {
        "title": "Finite-difference solvers, from the discretisation up",
        "org": "CSIR–National Aerospace Laboratories, Bengaluru",
        "role": "Research intern, Computational and Theoretical Fluid Dynamics division, 2026",
        "people": "Supervisor: V.&nbsp;K. Suman, Senior Principal Scientist",
        "body": [
            "Six modules written without CFD libraries, each scheme derived by hand, implemented in "
            "Python and then tested against something that could prove it wrong: the linear "
            "advection equation, spectral analysis of numerical error, two-dimensional advection, "
            "Burgers’ equation, Poisson’s equation and a lid-driven cavity in vorticity–streamfunction form.",
        ],
        "results": [
            "At Re&nbsp;=&nbsp;100 the cavity matches the Ghia et&nbsp;al. (1982) benchmark to 0.02&nbsp;% "
            "in vortex strength.",
            "At Re&nbsp;=&nbsp;400 and 1000 it misses by 6.6&nbsp;% and 16.3&nbsp;%, as the scheme’s "
            "modified equation predicted before the error was measured. Extrapolating the error away "
            "recovers the benchmark to 0.04&nbsp;% and 1.0&nbsp;%.",
            "At Re&nbsp;≥&nbsp;5000, two grids agree with each other while both sit far from the "
            "benchmark: a grid-independence study would have certified a wrong answer.",
        ],
        "repo": "cfd-from-scratch",
        "figure": ("fig-nal", "Lid-driven cavity at three Reynolds numbers: vorticity with streamfunction contours",
                   "The lid-driven cavity at Re&nbsp;=&nbsp;100, 400 and 1000: vorticity, with streamfunction contours."),
    },
    {
        "title": "Stagnation-point heating at Mach&nbsp;5",
        "org": "Advanced Systems Laboratory, DRDO, Hyderabad",
        "role": "Research intern, July to September 2025",
        "people": "Guided by Dr. Raj Kiran Grandhi and Mr. Mayank Gupta",
        "body": [
            "The heat flux at the nose of a blunt body, a hemisphere of radius 0.1&nbsp;m at Mach&nbsp;5 "
            "and 10&nbsp;km, predicted three ways: Fay–Riddell theory by hand, ANSYS Fluent, and CFD++ as "
            "an independent check, on structured meshes I made in Pointwise.",
        ],
        "results": [
            "Two independent solvers, on three meshes each, agree to ±2.3&nbsp;%: laminar CFD puts the "
            "stagnation-point heat flux at 1.11–1.16&nbsp;MW/m².",
            "The SST k–ω turbulence model gives six to nine times more. The boundary layer at a blunt "
            "nose is laminar, and a fully turbulent model adds transport the flow does not have. "
            "Finding that took about a month.",
            "Evaluated consistently, Fay–Riddell theory sits 10&nbsp;% below the CFD. My internship "
            "report had claimed 2&nbsp;%; rebuilding the calculation showed where that came from.",
        ],
        "repo": "hypersonic-stagnation-heating",
        "figure": ("fig-drdo", "Mach number around the nose and wall heat flux from two solvers against theory",
                   "Mach number around the nose, and the wall heat flux from both solvers against theory."),
    },
    {
        "title": "Engine subsystem, Formula Student",
        "org": "Ashwa Racing, RV College of Engineering",
        "role": "Engine subsystem engineer, since 2025",
        "people": "",
        "body": [
            "Ashwa Racing designs and builds the college’s Formula Student car. In 2025 I was "
            "responsible for the engine cooling calculation: I measured the radiator, fan and pump of its "
            "Suzuki GSX-R600 engine, modelled the radiator in SolidWorks and wrote the heat-rejection "
            "report. In 2026 I rebuilt it as a model of the whole coolant loop in MATLAB, with the "
            "Simulink version generated entirely by script. I am also redesigning the intake manifold for "
            "better airflow. In January 2026 the team competed at Formula Bharat, at the Kari Motor "
            "Speedway in Coimbatore.",
        ],
        "results": [
            "Over a 22&nbsp;km endurance run built to the Formula SAE rules, in 31&nbsp;°C air, the coolant "
            "peaks at 93.9&nbsp;°C and the fan never switches on, provided the duct brings 30&nbsp;% of the "
            "car’s speed to the core. At 15&nbsp;% the coolant would settle at 107&nbsp;°C, above the "
            "105&nbsp;°C limit.",
            "Checked line by line, my 2025 report reached the right conclusion with the wrong numbers: "
            "300&nbsp;CFM of air can carry at most 11.8&nbsp;kW, about half the 23.3&nbsp;kW the report "
            "credited the radiator with.",
            "The script-built Simulink model matches the plain MATLAB version to within "
            "4&nbsp;×&nbsp;10<sup>−13</sup>&nbsp;K at all 17,261 time steps of the event.",
        ],
        "repo": "formula-student-radiator-cooling",
        "photo": ("ashwa", "Uday Kiran beside a Formula Student car in the Ashwa Racing workshop",
                  "In the Ashwa Racing workshop, February 2025."),
    },
]

# ---------------------------------------------------------------- projects
PROJECTS_INTRO = (
    "Each project below is a public repository with its code, data and figures, and an honest "
    "account of what went wrong. Where a result we submitted did not survive a later check, the "
    "repository says so, and says why."
)

PROJECTS_LEAD = [
    {
        "title": "Turbopumps and nozzle for a Raptor-class rocket engine",
        "context": "Independent design study, 2025, completed in November 2026",
        "guide": "",
        "body": [
            "A 2&nbsp;MN full-flow staged-combustion engine burning liquid oxygen and methane, in the class "
            "of SpaceX’s Raptor. In 2025 I sized its nozzle with RPA, ran the nozzle in ANSYS Fluent and "
            "modelled both turbopumps in CFturbo. In 2026 I finished it in Python: equilibrium chemistry "
            "with Cantera, real-fluid properties with CoolProp, a power balance of the cycle and meanline "
            "sizing of the pumps and turbines.",
            "A published estimate of Raptor’s cycle, the one the turbopumps were built around, does not "
            "close: its methane turbine delivers 20.4&nbsp;MW to a pump that needs 28&nbsp;MW. Keeping its "
            "pressures, the shafts balance with the preburners at 708&nbsp;K and 897&nbsp;K instead of "
            "811&nbsp;K, and the 300&nbsp;bar thrust chamber gives 2.04&nbsp;MN at 333&nbsp;s at sea level. "
            "Checking the 2025 turbopumps against that cycle found eight problems, from a turbine designed "
            "for its exit conditions to a methane pump 34&nbsp;% short of head. The repository lists them all.",
        ],
        "repo": "raptor-class-engine-design",
        "figure": ("fig-raptor", "Flow schematic of the engine: two pumps, two preburners, two turbines and the main chamber",
                   "The balanced cycle. Each turbine drives its own pump; the oxygen-rich preburner runs at "
                   "708&nbsp;K and the fuel-rich one at 897&nbsp;K."),
    },
    {
        "title": "Roughness and the oblique shock on a supersonic double wedge",
        "context": "Gas Dynamics lab project, 6th semester, four students",
        "guide": "Guided by Bhaskar K",
        "body": [
            "Does a rough surface change the angle of an oblique shock? We put a 70&nbsp;mm double wedge "
            "in a Mach&nbsp;3 stream in ANSYS Fluent, with a smooth wall and with sand-grain roughness "
            "from 0.05 to 0.9&nbsp;mm, and compared the results with shock-expansion theory.",
            "Measured three independent ways in the saved solution, the smooth-wall shock sits at "
            "23.7°, 0.35° steeper than inviscid theory, because the outer flow sees a wedge thickened "
            "by the boundary layer. Rebuilding the project from the raw solver output also showed that "
            "our report’s hand reading of the shock, the Mach number it printed and its grid study were "
            "wrong. The repository says how.",
        ],
        "repo": "double-wedge-roughness",
        "figure": ("fig-gd", "Numerical schlieren of a double wedge at Mach 3 with the measured leading-edge shock",
                   "Numerical schlieren of the Mach&nbsp;3 smooth-wall solution, with the leading-edge shock "
                   "measured from the flow field."),
    },
    {
        "title": "Non-linear capture boundary for electromagnetic CubeSat docking",
        "context": "Mathematical Modelling experiential learning, 6th semester, four students",
        "guide": "Guided by Nivya Muchikel",
        "body": [
            "When does a magnet, a cone and a spring capture a docking CubeSat? Our July answer was a "
            "closed-form capture boundary. Checked against our own equations of motion, it did not hold: "
            "with the coil left on, the boundary is a separatrix through a saddle point, at "
            "0.094&nbsp;m/s, and at 4.95&nbsp;A a saddle-node bifurcation removes the capture well altogether.",
            "Switching the coil off at contact gives an exact closed form, 0.424&nbsp;m/s, which the "
            "simulation reproduces. A planar rigid-body model of the cone, with friction and contact, "
            "then shows which misalignments the design can take.",
        ],
        "repo": "cubesat-docking-capture-boundary",
        "figure": ("fig-mm", "Two phase portraits of the docking, with the separatrix and saddle point marked",
                   "Phase portraits of the docking. Left, coil on: the separatrix through the saddle divides "
                   "captured runs (green) from those pulled into the magnet (red). Right, coil off at contact: "
                   "a damped spring."),
    },
    {
        "title": "Radar cross section and stealth shaping, from scratch",
        "context": "Avionics project-based learning, 6th semester, three students",
        "guide": "Guided by Dr. Rachana Akki and Dr. Karthik Vel E",
        "body": [
            "How strongly does an aircraft send a radar pulse back, and why do stealth aircraft look the "
            "way they do? We built four aircraft from flat triangles and wrote the electromagnetics in "
            "Python with the free version of Claude, one attempt after another: Physical Optics, edge "
            "diffraction, double and triple bounces, and radar-absorbing materials.",
            "Checked in November 2026 against answers known exactly, two results we had presented, a "
            "sphere check and a headline reduction, did not hold up, and the solver has been corrected.",
        ],
        "repo": "rcs-stealth-geometries",
        "figure": ("fig-rcs", "Top, side and front views of four faceted aircraft models",
                   "Top, side and front views of the four aircraft: conventional, stealth, flying wing and "
                   "chined nose, each made of 18 to 32 flat facets."),
    },
]

PROJECTS_MORE = [
    {
        "title": "Conjunction screening for a LEO digital twin",
        "context": "Interdisciplinary project, 6th semester, two aerospace and two information science students",
        "guide": "",
        "body": [
            "The aerospace half of the project: propagation and conjunction screening in STK for 33 "
            "satellites, then open-source code that checks every number STK gave. Free SGP4 reproduces "
            "STK’s ephemerides to within 1.3&nbsp;mm, and a screener written from scratch reproduces its "
            "close approaches to 1&nbsp;mm. The digital twin itself is my teammates’ work, in "
            "<a href=\"https://github.com/KhushiChoudki/Energy-Aware-Digital-Twin-of-LEO-Satellite-Constellations-Using-Scalable-N-Body-Simulation-\">their repository</a>.",
        ],
        "repo": "leo-conjunction-screening",
        "figure": ("fig-leo", "STK globe view of satellite orbits over Asia",
                   "The STK scenario: 33 satellites in low Earth orbit, 15 of them Indian."),
    },
    {
        "title": "A spinning porous-blade deaerator",
        "context": "Computational Fluid Dynamics experiential learning, 6th semester, four students",
        "guide": "Guided by Bhaskar K",
        "body": [
            "A deaerator for the fuel and water separation system of the LCA Tejas, from a short problem "
            "statement: a porous rotor turning at 1000&nbsp;rpm separates water from air. We meshed "
            "a quarter of the disc in Pointwise and used rotational periodicity and the mixture model in "
            "ANSYS Fluent. After 0.6&nbsp;s the water had gathered in a layer about 2&nbsp;mm thick on the casing.",
        ],
        "repo": "deaerator-rotating-porous-blade",
        "figure": ("fig-deaer", "Water volume fraction over a spinning porous disc",
                   "Water volume fraction over the whole disc, built from the computed quarter."),
    },
    {
        "title": "A variable-pitch propeller on a home-built thrust bench",
        "context": "Aerospace Propulsion project-based lab, 4th semester, five students",
        "guide": "Guided by Dr. Supreeth R",
        "body": [
            "A servo turns two blades in a 3D-printed hub; a wooden bench measures the thrust with a "
            "5&nbsp;kg load cell, a laser tachometer and four Arduinos. At about 3000&nbsp;rpm it gave 102&nbsp;g "
            "of thrust at 2° of pitch and 202&nbsp;g at 15°. Our most hands-on project, and our first CFD.",
        ],
        "repo": "variable-pitch-propeller",
        "figure": ("fig-prop", "A propeller with a 3D-printed hub on a wooden test stand",
                   "The bench: the motor and printed hub on the left post; on the right, the servo and the "
                   "rack that turn the blades."),
    },
    {
        "title": "Holding a model aircraft cabin at 30&nbsp;°C",
        "context": "Aircraft Systems and Instrumentation experiential learning, 5th semester, four students",
        "guide": "Guided by Gp Capt Deepak Bana VSM (Retd)",
        "body": [
            "A very small environmental control system: a cardboard cabin with a nichrome heater, a fan "
            "and a DHT11 sensor, controlled by an STM32 Nucleo running a three-band thermostat. Simple on "
            "paper; making every part work together took from October to February.",
        ],
        "repo": "stm32-ecs-temperature-control",
        "figure": ("fig-ecs", "A control box with an STM32 board and relays next to a cardboard cabin",
                   "The finished system, January 2026: the control box and the cabin."),
    },
]

OTHER_WORK = (
    "Not written up yet: two-way fluid–structure interaction of a flat plate with dynamic meshing; a "
    "NACA&nbsp;0012 study with a grid-independence check; a satellite nadir-pointing system; an explicit "
    "dynamics contact analysis; foamforge, an offline generator of OpenFOAM cases with a 23-test suite; "
    "and a physics-informed neural network for unsteady heat conduction."
)

# ---------------------------------------------------------------- path
PATH_TITLE = "Four years at RVCE"

PATH_TEXT = [
    "My four years at RVCE have taken the work steadily deeper. In the first year I learnt to draw and "
    "model parts, and built a quadcopter and a fixed-wing aircraft with classmates. In the second I built "
    "hardware that had to work on a bench, a variable-pitch propeller and its thrust stand, joined the "
    "engine subsystem of our Formula Student team, where I worked on the radiator, and began a design "
    "study of a rocket engine’s turbopumps and nozzle.",
    "In the third year I moved to simulation: hypersonic stagnation heating at DRDO, then shocks over a "
    "rough double wedge, a rotating porous deaerator, the dynamics of CubeSat docking, radar scattering "
    "from aircraft shapes and satellite conjunction screening in my sixth-semester projects.",
    "In the fourth I went to the methods underneath. At CSIR–NAL I wrote finite-difference solvers from "
    "the discretisation up and learnt to predict a scheme’s error before measuring it. Since November "
    "2026 I have been publishing every project in full, including what went wrong, and finishing the "
    "two I had left undone: the rocket engine study and the radiator model.",
]

PATH_BEYOND = (
    "Outside the lab I am a member of the RVCE Debating Society and of CubeX, the college "
    "speedcubing club, and I have volunteered as a scrambler at three official World Cube "
    "Association competitions. I have also run two 10&nbsp;km runs organised by RVCE."
)

YEARS = [
    ("Before RVCE", "2020–23", "Teaching and mathematics", [
        ("2020–21", "Taught mathematics to Grades 1–10 at Sidda Samadhi Yoga Gurukul"),
        ("2021–22", "Trained for mathematics competitions"),
        ("", "Started a physics degree at Manipal, then left it for aerospace engineering"),
        ("2023", "Master Certificate in Product Design, CADD Centre: AutoCAD, CATIA, Ansys"),
    ]),
    ("Year 1", "2023–24", "Drawing and building", [
        ("", "Started B.E. Aerospace Engineering at RVCE"),
        ("", "Team Antariksh, the college satellite team, where I learnt SolidWorks and LaTeX"),
        ("", "Built a quadcopter and a fixed-wing aircraft with classmates, for an experiential-learning project"),
        ("July 2024", "Top Performer, Assembly Wiz CAD competition"),
    ]),
    ("Year 2", "2024–25", "Hardware that has to work", [
        ("2025", "Joined Ashwa Racing, engine subsystem"),
        ("2025", "1st Runner Up, Vyoma Design-a-thon"),
        ("April–Aug 2025", "Raptor-class engine study: nozzle in RPA and Fluent, turbopumps in CFturbo"),
        ("May–July 2025", "Variable-pitch propeller and thrust bench, and my first CFD"),
        ("July 2025", "Radiator measurements and cooling report for Ashwa Racing"),
        ("July 2025", "HAL Aerothon ’25"),
    ]),
    ("Year 3", "2025–26", "Simulation", [
        ("July–Sept 2025", "Research intern, DRDO Advanced Systems Laboratory: hypersonic heating in Fluent and CFD++"),
        ("Oct 2025–Feb 2026", "STM32 cabin temperature control"),
        ("January 2026", "Formula Bharat with Ashwa Racing"),
        ("6th semester", "Double wedge, CubeSat docking, radar cross section, deaerator and conjunction screening"),
        ("June 2026", "International Certificate Course on Six Sigma"),
    ]),
    ("Year 4", "2026–27", "The numerics underneath", [
        ("2026", "Research intern, CSIR–National Aerospace Laboratories: finite-difference solvers from scratch"),
        ("November 2026", "Started publishing my projects on GitHub"),
        ("November 2026", "Finished the rocket engine study and the radiator model"),
        ("", "Applying for MS programmes for autumn 2027"),
    ]),
]

# ---------------------------------------------------------------- awards
AWARDS = [
    ("2025", "1st Runner Up, Vyoma Design-a-thon, RVCE"),
    ("July 2024", "Top Performer, Assembly Wiz, the Computer Aided Engineering Graphics competition of "
                  "the Department of Mechanical Engineering, RVCE"),
    ("2023", "Timed mathematical puzzle-solving: 1st in Bengaluru and in Karnataka, 34th in India and "
             "69th in Asia"),
]

COMPETITIONS = [
    ("June 2026", "International Certificate Course on Six Sigma, delivered at RVCE by Rose-Hulman "
                  "Institute of Technology, USA"),
    ("January 2026", "Competed at Formula Bharat 2026 with Ashwa Racing, Kari Motor Speedway, Coimbatore"),
    ("July 2025", "Took part in HAL Aerothon ’25, a two-day hackathon on a digital twin of a fuel-injection "
                  "system, organised by Hindustan Aeronautics Limited and PES University"),
    ("2023", "Master Certificate in Product Design (AutoCAD, CATIA, Ansys), CADD Centre"),
]

AWARD_PHOTOS = [
    ("vyoma", "Uday Kiran receiving a certificate from Dr. Ravindra S Kulkarni",
     "Receiving my certificate at the Vyoma Design-a-thon from Dr. Ravindra S Kulkarni, then Head of "
     "Aerospace Engineering at RVCE. 2025."),
    ("assemblywiz", "Uday Kiran receiving a medal and certificate from Dr. Shanmukha Nagaraj",
     "Receiving the Top Performer award at Assembly Wiz from Dr. Shanmukha Nagaraj, then Dean of "
     "Academics at RVCE. July 2024."),
]

# ---------------------------------------------------------------- tools
COURSEWORK = (
    "Gas Dynamics, Computational Fluid Dynamics, Mathematical Modelling, Thermodynamics, and Statistics, "
    "Laplace Transform and Numerical Methods: all O. Mechanics of Fluids, Aerospace Propulsion, Aerospace "
    "Structures, Finite Element Methods, Structural Dynamics and Avionics: all A+."
)
COURSEWORK_NOTE = "O is the top grade on the college’s 10-point scale, and A+ the next."

TOOLS = [
    ("CFD and meshing", "ANSYS Fluent, CFD++, OpenFOAM, COMSOL Multiphysics, Pointwise, HyperMesh, Gmsh"),
    ("Numerical methods", "Finite-difference and finite-volume schemes; von Neumann stability, order of "
                          "accuracy and convergence; modified-equation and spectral analysis of numerical error"),
    ("Programming", "Python (NumPy, SciPy, Matplotlib, PyTorch), C, MATLAB, Bash, Git, LaTeX, gnuplot"),
    ("Propulsion", "RPA, CFturbo, Cantera and CoolProp: equilibrium chemistry, nozzle design, cycle "
                   "power balance and meanline turbomachinery"),
    ("Structures and systems", "ANSYS Mechanical, APDL and Explicit Dynamics, Nastran/Patran, STK, HFSS, "
                               "Simulink"),
    ("Design and making", "SolidWorks, CATIA, Fusion, FreeCAD; CNC and lathe machining, casting, FDM and "
                          "SLA 3D printing; Arduino and STM32"),
]

# ---------------------------------------------------------------- contact
CONTACT_TEXT = (
    "The best way to reach me is by email. I am also on "
    f"<a href=\"{LINKEDIN}\">LinkedIn</a> and <a href=\"{GITHUB}\">GitHub</a>."
)
