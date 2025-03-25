<?xml version="1.0" encoding="UTF-8"?>
<MetaResultFile version="20211011" creator="FE Port mode solver">
  <MetaGeometryFile filename="" lod="1"/>
  <SimulationProperties fieldname="Zmax Out p1" frequency="0" encoded_unit="&amp;U:V^1.:A^1.:m^-2" quantity="powerflow" fieldtype="Powerflow" fieldscaling="TIME_AVERAGE" dB_Amplitude="10"/>
  <ResultDataType vector="1" complex="0" timedomain="0" frequencymap="1"/>
  <SimulationDomain min="0 0 0" max="0 0 0"/>
  <PlotSettings Plot="1" ignore_symmetry="0" deformation="0" enforce_culling="0" integer_values="0" combine="CombineNone" default_arrow_type="ARROWS" default_scaling="NONE">
    <Plane normal="0 0 1" distance="2.91761971"/>
  </PlotSettings>
  <Source type="SOLVER"/>
  <SpecialMaterials>
    <Background type="NORMAL"/>
  </SpecialMaterials>
  <AuxGeometryFile/>
  <AuxResultFile/>
  <FieldFreeNodes/>
  <SurfaceFieldCoefficients/>
  <UnitCell/>
  <SubVolume/>
  <Units/>
  <ProjectUnits/>
  <TimeSampling/>
  <LocalAxes/>
  <MeshViewSettings/>
  <ResultGroups num_steps="3" transformation="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1" process_mesh_group="0">
    <SharedDataWith/>
    <Frame index="0" characteristic="32">
      <PortModeInfoFile filename="Port2_Info1(#0000).mmd"/>
      <FieldResultFile filename="Port2_pout1(#0000).sct" type="sct" meshname="Port2.slim"/>
    </Frame>
    <Frame index="1" characteristic="26">
      <PortModeInfoFile filename="Port2_Info1(#0001).mmd"/>
      <FieldResultFile filename="Port2_pout1(#0001).sct" type="sct" meshname="Port2.slim"/>
    </Frame>
    <Frame index="2" characteristic="29">
      <PortModeInfoFile filename="Port2_Info1(#0002).mmd"/>
      <FieldResultFile filename="Port2_pout1(#0002).sct" type="sct" meshname="Port2.slim"/>
    </Frame>
  </ResultGroups>
  <AutoScale>
    <SmartScaling log_strength="1" log_anchor="0" log_anchor_type="0" db_range="40" phase="0"/>
  </AutoScale>
</MetaResultFile>
