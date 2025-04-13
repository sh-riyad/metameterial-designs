'# MWS Version: Version 2024.1 - Oct 16 2023 - ACIS 33.0.1 -

'# length = mm
'# frequency = GHz
'# time = s
'# frequency range: fmin = 20.0 fmax = 32.0
'# created = '[VERSION]2024.1|33.0.1|20231016[/VERSION]


'@ define units

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Units
.SetUnit "Length", "mm"
.SetUnit "Temperature", "K"
.SetUnit "Voltage", "V"
.SetUnit "Current", "A"
.SetUnit "Resistance", "Ohm"
.SetUnit "Conductance", "S"
.SetUnit "Capacitance", "pF"
.SetUnit "Inductance", "nH"
.SetUnit "Frequency", "GHz"
.SetUnit "Time", "s"
.SetResultUnit "frequency", "frequency", ""
End With

'@ define material: FR4 (Lossy)

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Material
.Reset
.Name "FR4 (Lossy)"
.Type "Normal"
.Epsilon "4.3"
.Mue "1.0"
.TanD "0.025"
.TanDFreq "0.0"
.TanDGiven "True"
.TanDModel "ConstTanD"
.Sigma "0.0"
.TanDM "0.0"
.TanDMFreq "0.0"
.TanDMGiven "False"
.TanDMModel "ConstTanD"
.SigmaM "0.0"
.Colour "0.940000", "0.820000", "0.760000"
.Create
End With

'@ define material: Copper (pure)

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Material
.Reset
.Name "Copper (pure)"
.Type "Normal"
.Epsilon "1.0"
.Mue "1.0"
.TanD "0.0"
.TanDFreq "0.0"
.TanDGiven "False"
.TanDModel "ConstTanD"
.Sigma "59600000.0"
.TanDM "0.0"
.TanDMFreq "0.0"
.TanDMGiven "False"
.TanDMModel "ConstTanD"
.SigmaM "0.0"
.Colour "0.850000", "0.550000", "0.200000"
.Create
End With

'@ define brick: Substrate

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Brick
.Reset
.Name "Substrate"
.Component "component1"
.Material "FR4 (Lossy)"
.XRange "-8.0", "8.0"
.YRange "-8.0", "8.0"
.ZRange "-1.6", "0.0"
.Create
End With

'@ define brick: Outer Box

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Brick
.Reset
.Name "Outer Box"
.Component "component1"
.Material "Copper (pure)"
.XRange "-7.65", "7.65"
.YRange "-7.65", "7.65"
.ZRange "0.0", "0.035"
.Create
End With

'@ define brick: Cut1

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Brick
.Reset
.Name "Cut1"
.Component "component1"
.Material "Copper (pure)"
.XRange "-6.65", "6.65"
.YRange "-6.65", "6.65"
.ZRange "0.0", "0.035"
.Create
End With

'@ boolean subtract shapes: component1:Outer Box, component1:Cut1

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
Solid.Subtract "component1:Outer Box", "component1:Cut1"

'@ define brick: Cut2

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Brick
.Reset
.Name "Cut2"
.Component "component1"
.Material "Copper (pure)"
.XRange "-0.5", "0.5"
.YRange "-8.15", "8.15"
.ZRange "0.0", "0.035"
.Create
End With

'@ boolean subtract shapes: component1:Outer Box, component1:Cut2

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
Solid.Subtract "component1:Outer Box", "component1:Cut2"

'@ define brick: Cut3

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Brick
.Reset
.Name "Cut3"
.Component "component1"
.Material "Copper (pure)"
.XRange "-8.15", "8.15"
.YRange "-0.5", "0.5"
.ZRange "0.0", "0.035"
.Create
End With

'@ boolean subtract shapes: component1:Outer Box, component1:Cut3

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
Solid.Subtract "component1:Outer Box", "component1:Cut3"

'@ define cylinder: Outer Circle

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Cylinder
.Reset
.Name "Outer Circle"
.Component "component1"
.Material "Copper (pure)"
.OuterRadius "6.0"
.InnerRadius "5.0"
.Axis "z"
.Zrange "0.0", "0.035"
.Xcenter "0.0"
.Ycenter "0.0"
.Segments "0"
.Create
End With

'@ define brick: Cut4

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Brick
.Reset
.Name "Cut4"
.Component "component1"
.Material "Copper (pure)"
.XRange "-0.5", "0.5"
.YRange "-6.0", "6.0"
.ZRange "0.0", "0.035"
.Create
End With

'@ boolean subtract shapes: component1:Outer Circle, component1:Cut4

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
Solid.Subtract "component1:Outer Circle", "component1:Cut4"

'@ define brick: Cut5

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Brick
.Reset
.Name "Cut5"
.Component "component1"
.Material "Copper (pure)"
.XRange "-6.0", "6.0"
.YRange "-0.5", "0.5"
.ZRange "0.0", "0.035"
.Create
End With

'@ boolean subtract shapes: component1:Outer Circle, component1:Cut5

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
Solid.Subtract "component1:Outer Circle", "component1:Cut5"

'@ define brick: Inner Box

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Brick
.Reset
.Name "Inner Box"
.Component "component1"
.Material "Copper (pure)"
.XRange "-3.0", "3.0"
.YRange "-3.0", "3.0"
.ZRange "0.0", "0.035"
.Create
End With

'@ define brick: Cut6

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Brick
.Reset
.Name "Cut6"
.Component "component1"
.Material "Copper (pure)"
.XRange "-0.5", "0.5"
.YRange "-3.0", "3.0"
.ZRange "0.0", "0.035"
.Create
End With

'@ boolean subtract shapes: component1:Inner Box, component1:Cut6

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
Solid.Subtract "component1:Inner Box", "component1:Cut6"

'@ define cylinder: Cut7

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Cylinder
.Reset
.Name "Cut7"
.Component "component1"
.Material "Copper (pure)"
.OuterRadius "2.5"
.InnerRadius "2.0"
.Axis "z"
.Zrange "0.0", "0.035"
.Xcenter "0.0"
.Ycenter "0.0"
.Segments "0"
.Create
End With

'@ boolean subtract shapes: component1:Inner Box, component1:Cut7

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
Solid.Subtract "component1:Inner Box", "component1:Cut7"

'@ define frequency range

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
Solver.FrequencyRange "20.0", "32.0"

'@ define boundaries

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With Boundary
.Xmin "unit cell"
.Xmax "unit cell"
.Ymin "unit cell"
.Ymax "unit cell"
.Zmin "expanded open"
.Zmax "expanded open"
.ApplyInAllDirections "False"
.OpenAddSpaceFactor "0.5"
End With

'@ define Floquet Port boundaries

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
With FloquetPort
.Reset
.SetPolarizationIndependentOfScanAnglePhi "0.0", "False"
.SetSortCode "+beta/pw"
.SetCustomizedListFlag "False"
.Port "Zmin"
.SetNumberOfModesConsidered "1"
.SetDistanceToReferencePlane "0.0"
.SetUseCircularPolarization "False"
.Port "Zmax"
.SetNumberOfModesConsidered "1"
.SetDistanceToReferencePlane "0.0"
.SetUseCircularPolarization "False"
End With
With Boundary
.SetPeriodicBoundaryAngles "0.0", "0.0"
.SetPeriodicBoundaryAnglesDirection "outward"
End With

'@ change solver type

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
ChangeSolverType "HF Frequency Domain"

'@ set stimulation

'[VERSION]2024.1|33.0.1|20231016[/VERSION]
FDSolver.Stimulation "Zmin", "TE(0,0)"

