## Customize Makefile settings for copi
##
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

# Override base target: generated Makefile uses $(URIBASE)/COPI (uppercase, no path)
# which does not match actual COPI IRIs (https://www.inf.ufrgs.br/ontologies/copi/...).
$(ONT)-base.owl: $(EDIT_PREPROCESSED) $(OTHER_SRC) $(IMPORT_FILES)
	$(ROBOT_RELEASE_IMPORT_MODE) \
	reason --reasoner $(REASONER) --equivalent-classes-allowed asserted-only --exclude-tautologies structural --annotate-inferred-axioms false \
	relax $(RELAX_OPTIONS) \
	reduce -r $(REASONER) $(REDUCE_OPTIONS) \
	remove --base-iri $(ONTBASE) --axioms external --preserve-structure false --trim false \
	$(SHARED_ROBOT_COMMANDS) \
	annotate --link-annotation http://purl.org/dc/elements/1.1/type http://purl.obolibrary.org/obo/IAO_8000001 \
		--ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		--output $@.tmp.owl && mv $@.tmp.owl $@
