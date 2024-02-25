class ModelConfigurationOption(models.Model):
    FIELD_TYPE_CHOICE = (
        ('number', 'number'),
        ('text', 'text'),
        ('choice', 'choice'),
        ('group', 'group')
    )
    tool_model = models.ForeignKey("ToolModel", blank=True, on_delete=models.CASCADE, null=True,
                                   help_text="the original model")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, null=True,
                               related_name='model_config_child_options')
    referenced_option = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, null=True,
                                          related_name='descriptor_options',
                                          help_text="number multiplier used for choice option material qty")
    field_name = models.TextField(default='')
    field_type = models.CharField(
        max_length=100, choices=FIELD_TYPE_CHOICE, default='text')

    identifier = models.CharField(
        max_length=20, default="", help_text="unique identifier used for reverse lookup")

    is_required = models.BooleanField(
        default=True, help_text=_("indicate if option is required"))

    ordering = models.IntegerField(blank=True, null=True, default=1)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class ModelConfigurationOptionChoice(models.Model):
    model_configuration_option = models.ForeignKey("ModelConfigurationOption", blank=True, on_delete=models.CASCADE,
                                                   null=True, help_text="the original model", related_name='option_choices')
    choice_name = models.TextField(default='')
    choice_code = models.CharField(max_length=100, default='')

    ordering = models.IntegerField(blank=True, null=True, default=1)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class ModelConfigurationOptionChoiceDependency(models.Model):
    parent_choice = models.ForeignKey("ModelConfigurationOptionChoice", blank=True, on_delete=models.CASCADE, null=True,
                                      related_name='parent_choice_dependency')
    child_choice = models.ForeignKey("ModelConfigurationOptionChoice", blank=True, on_delete=models.CASCADE, null=True,
                                     related_name='child_choice_dependency')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)



ModelConfigurationOption.objects.prefetch(
    Prefetch('option_choices', ModelConfigurationOptionChoice.objects.prefetch(
        Prefetch('parent_choice_dependency', ModelConfigurationOptionChoiceDependency.objects.select_related('parent_choice', 'child_choice')),
        Prefetch('child_choice_dependency', ModelConfigurationOptionChoiceDependency.objects.select_related('parent_choice', 'child_choice'))
        )
    )
)


class DependencyModelConfigurationOptionChoiceSerializer(serializer.ModelSerialiser):

    class Meta:
        model = ModelConfigurationOptionChoice
        fields = ('id', 'model_configuration_option_id', 'choice_name', 'choice_code', 'ordering')
        read_pnly_dileds = fields


class ModelConfigurationOptionChoiceDependencySerializer(serializer.ModelSerialiser):
    prent_choice = DependencyModelConfigurationOptionChoiceSerializer()
    child_choice = DependencyModelConfigurationOptionChoiceSerializer()

    class Meta:
        model = ModelConfigurationOptionChoiceDependency
        fields = ('id', 'prent_choice', 'child_choice')
        read_pnly_dileds = fields


class ModelConfigurationOptionChoiceSerializer(serializer.ModelSerialiser):
    parent_choice_dependency = ModelConfigurationOptionChoiceDependencySerializer(many=True)
    child_choice_dependency = ModelConfigurationOptionChoiceDependencySerializer(many=True)

    class Meta:
        model = ModelConfigurationOptionChoice
        fields = ('id', 'choice_name', 'choice_code', 'ordering', 'parent_choice_dependency', 'child_choice_dependency')
        read_pnly_dileds = fields


class ModelConfigurationOptionSerializer(serializer.ModelSerialiser):
    option_choices = ModelConfigurationOptionChoiceSerializer(many=True)

    class Meta:
        model = ModelConfigurationOption
        fields = ('id', 'option_choices', )
        read_pnly_dileds = fields




