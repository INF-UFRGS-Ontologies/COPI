## Customize Makefile settings for copi
##
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

# Override mirror-iof-core: generated Makefile has 202601; correct version is 202602.
# Remove this override after `sh run.sh make update` regenerates the main Makefile.
.PHONY: mirror-iof-core
mirror-iof-core: | $(TMPDIR)
	$(ROBOT) convert -I https://spec.industrialontologies.org/ontology/202602/core/Core/ -o $(TMPDIR)/$@.owl

# ODR-015: component files (editorial; pending odk.py update regeneration)
COMPONENT_FILES = $(COMPONENTSDIR)/copi-core.ttl $(COMPONENTSDIR)/copi-vocab.ttl $(COMPONENTSDIR)/copi-enriched.owl
OTHER_SRC = $(COMPONENT_FILES)

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

# Override copi.owl and copi.ttl IRIs: use $(ONTBASE)/copi.{owl,ttl}
# = https://www.inf.ufrgs.br/ontologies/copi/copi.owl  (ODR-015 IRI canonical)
$(ONT).owl: $(ONT)-full.owl
	$(ROBOT) annotate --input $< --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert -o $@.tmp.owl && mv $@.tmp.owl $@

$(ONT).ttl: $(ONT).owl
	$(ROBOT) annotate --input $< --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert --check false -f ttl -o $@.tmp.ttl && mv $@.tmp.ttl $@

# Scoped HermiT guard target (ODR-015)
# Merges copi-core + copi-vocab + copi-enriched + mirrors; reasons with HermiT;
# then verifies 10 violation-style SPARQL guards.
GUARD_QUERIES = $(wildcard ../sparql/guards/guard-*.sparql)
REASONED_GRAPH = $(TMPDIR)/reasoned-copi.owl

$(REASONED_GRAPH): $(COMPONENT_FILES) | $(TMPDIR)
	$(ROBOT) merge \
		-i mirror/bfo.owl \
		-i mirror/iof-core.owl \
		-i $(COMPONENTSDIR)/copi-core.ttl \
		-i $(COMPONENTSDIR)/copi-vocab.ttl \
		-i $(COMPONENTSDIR)/copi-enriched.owl \
		reason --reasoner HermiT \
			--equivalent-classes-allowed asserted-only \
			--exclude-tautologies structural \
		-o $@

.PHONY: guards
guards: $(REASONED_GRAPH)
	$(ROBOT) verify -i $< \
		--queries $(GUARD_QUERIES) \
		-O $(REPORTDIR)
	@echo "All COPI guards passed."
