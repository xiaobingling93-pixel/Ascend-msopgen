namespace ops {
class AddAscendC : public OpDef {
 public:
  explicit AddAscendC(const char *name) : OpDef(name) {
    this->Input("x")
        .ParamType(REQUIRED)
        .DataType({ge::DT_FLOAT})
        .Format({ge::FORMAT_ND})
        .UnknownShapeFormat({ge::FORMAT_ND});
    this->Input("y")
        .ParamType(REQUIRED)
        .DataType({ge::DT_FLOAT})
        .Format({ge::FORMAT_ND})
        .UnknownShapeFormat({ge::FORMAT_ND});
    this->Output("z")
        .ParamType(REQUIRED)
        .DataType({ge::DT_FLOAT})
        .Format({ge::FORMAT_ND})
        .UnknownShapeFormat({ge::FORMAT_ND});
    this->Attr("test").ListInt();
    this->Attr("required").AttrType(REQUIRED).String();
    this->Attr("p").AttrType(OPTIONAL).Int(2);
    this->Attr("axes").AttrType(OPTIONAL).ListInt({1});
    this->Attr("keepdim").AttrType(OPTIONAL).Bool(false);
    this->Attr("epsilon").AttrType(OPTIONAL).Float(1e-12);
    this->SetInferShape(ge::InferShape).SetInferShapeRange(ge::InferShapeRange).SetInferDataType(ge::InferDataType);

    this->AICore()
        .SetTiling(optiling::TilingFunc)
        .SetCheckSupport(optiling::check_op_support);

    OpAICoreConfig aicConfig;
    aicConfig.DynamicCompileStaticFlag(true)
        .DynamicFormatFlag(true)
        .DynamicRankSupportFlag(true)
        .DynamicShapeSupportFlag(true)
        .NeedCheckSupportFlag(true)
        .PrecisionReduceFlag(true);
    this->AICore().AddConfig("ascend910", aicConfig);
  }
};
}

