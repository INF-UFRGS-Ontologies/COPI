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

# Canonical ontology IRI = namespace URI (without filename suffix)
# = https://www.inf.ufrgs.br/ontologies/copi/
# index.php handles content negotiation at this URI.
$(ONT).owl: $(ONT)-full.owl
	$(ROBOT) annotate --input $< --ontology-iri $(ONTBASE)/ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert -o $@.tmp.owl && mv $@.tmp.owl $@

$(ONT).ttl: $(ONT).owl
	$(ROBOT) annotate --input $< --ontology-iri $(ONTBASE)/ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert --check false -f ttl -o $@.tmp.ttl && mv $@.tmp.ttl $@

# Scoped HermiT guard target (ODR-015)
# Merges copi-core + copi-vocab + copi-enriched + mirrors; reasons with HermiT;
# then verifies violation-style SPARQL guards.
# CHAIN_TEST_ABOX is test-only: not in OTHER_SRC, not imported by copi-edit.owl,
# does not appear in any release artefact.
GUARD_QUERIES = $(wildcard ../sparql/guards/guard-*.sparql)
REASONED_GRAPH = $(TMPDIR)/reasoned-copi.owl
CHAIN_TEST_ABOX = test/chain-participates-in-abox.ttl

$(REASONED_GRAPH): $(OTHER_SRC) $(CHAIN_TEST_ABOX) | $(TMPDIR)
	$(ROBOT) merge \
		-i mirror/bfo.owl \
		-i mirror/iof-core.owl \
		-i $(COMPONENTSDIR)/copi-core.ttl \
		-i $(COMPONENTSDIR)/copi-vocab.ttl \
		-i $(COMPONENTSDIR)/copi-enriched.owl \
		-i $(COMPONENTSDIR)/copi-floc.ttl \
		-i $(CHAIN_TEST_ABOX) \
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

# ----------------------------------------
# Standalone module: copi-floc (ODR-015)
# ----------------------------------------
# copi-floc is BOTH a COPI component (merged into the copi-* release artefacts
# through copi-edit.owl) AND a module importable on its own: it imports only BFO
# and IOF-Core, so an ontology outside oil and gas can reuse the functional
# location pattern without pulling in COPI's equipment taxonomy. These targets
# publish that standalone form; they are built by all_odk and copied to the
# release directory with the other release assets.

MODULE_PRODUCTS = copi-floc.owl copi-floc.ttl
RELEASE_ASSETS += $(MODULE_PRODUCTS)
all_odk: $(MODULE_PRODUCTS)

# Published WITHOUT merging the import closure (unlike copi-full): the point of
# the module is that it imports BFO 2020 and IOF-Core only, so importers resolve
# those themselves instead of receiving a second copy of them. The component's
# own owl:versionInfo is kept as the module's semantic version; the release adds
# only the dated versionIRI.
copi-floc.owl: $(COMPONENTSDIR)/copi-floc.ttl
	$(ROBOT) annotate --input $< \
		--ontology-iri $(ONTBASE)/$@ \
		--version-iri $(ONTBASE)/releases/$(VERSION)/$@ \
		convert -o $@.tmp.owl && mv $@.tmp.owl $@

copi-floc.ttl: $(COMPONENTSDIR)/copi-floc.ttl
	$(ROBOT) annotate --input $< \
		--ontology-iri $(ONTBASE)/$@ \
		--version-iri $(ONTBASE)/releases/$(VERSION)/$@ \
		convert --check false -f ttl -o $@.tmp.ttl && mv $@.tmp.ttl $@

.PHONY: modules
modules: $(MODULE_PRODUCTS)
