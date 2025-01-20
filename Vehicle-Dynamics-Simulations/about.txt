Overview
This project explores the dynamic behavior of vehicles under various configurations, analyzing handling and stability using a range of mathematical models and simulations. The work focuses on understanding how suspension properties, roll steer coefficients, and tire characteristics affect vehicle performance at different speeds. By employing both linear and nonlinear models with 2-DOF and 3-DOF systems, the study examines the impact of steering inputs and roll dynamics on yaw rate, drift angle, and stability.

The simulations were executed in MATLAB, leveraging state-space models and custom algorithms to explore steady-state and transient responses. Key results highlight the interplay between speed, suspension characteristics, and vehicle balance, providing insights into the understeer and oversteer dynamics that define handling behavior.

Key Objectives
Investigate the impact of speed on yaw rate and drift angle.
Analyze the influence of roll steer coefficients on vehicle stability and responsiveness.
Compare linear and nonlinear tire models for different suspension setups.
Explore the effects of front and rear bias configurations on handling characteristics.
Methodology
The project employed a combination of theoretical modeling and computational simulation:

Linear Models: Used 2-DOF and 3-DOF state-space equations to study basic dynamics and validate stability at varying speeds.
Nonlinear Models: Factored in tire stiffness and body roll to simulate real-world conditions, capturing complex oscillatory behavior at high speeds.
Parametric Analysis: Examined front and rear suspension roll steer biases, identifying configurations that maximize stability or responsiveness.
The MATLAB code implemented time-domain simulations, iterating through multiple scenarios to capture the nuanced effects of different design parameters.

Highlights & Results
Increasing speed amplifies understeer, while roll steer coefficients significantly influence stability.
A 60/40 front bias creates a more stable, understeering vehicle, while a 40/60 rear bias induces oversteer and instability beyond 60 mph.
Nonlinear tire models introduce oscillatory responses due to body roll effects, offering more realistic insights compared to linear assumptions.
Roll stiffness (Kφ) and damping (Dφ) were found to be key factors in balancing stability and responsiveness.
Graphs of yaw rate, drift angle, and stability responses demonstrate the effects of various configurations, providing valuable data for vehicle tuning and design optimization.
