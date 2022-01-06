const ID_RE = /(-)_(-)/;

            /**
             * Replace the template index of an element (-_-) with the
             * given index.
             */
            function replaceTemplateIndex(value, index) {
                return value.replace(ID_RE, '$1'+index+'$2');
            }

            /**
             * Adjust the indices of form fields when removing items.
             */
            function adjustIndices(removedIndex) {
                var $forms = $('.subform');

                $forms.each(function(i) {
                    var $form = $(this);
                    var index = parseInt($form.data('index'));
                    var newIndex = index - 1;

                    if (index < removedIndex) {
                        // Skip
                        return true;
                    }

                    // This will replace the original index with the new one
                    // only if it is found in the format -num-, preventing
                    // accidental replacing of fields that may have numbers
                    // intheir names.
                    var regex = new RegExp('(-)'+index+'(-)');
                    var repVal = '$1'+newIndex+'$2';

                    // Change ID in form itself
                    $form.attr('id', $form.attr('id').replace(index, newIndex));
                    $form.data('index', newIndex);

                    // Change IDs in form fields
                    $form.find('label, input, select, textarea').each(function(j) {
                        var $item = $(this);

                        if ($item.is('label')) {
                            // Update labels
                            $item.attr('for', $item.attr('for').replace(regex, repVal));
                            return;
                        }

                        // Update other fields
                        $item.attr('id', $item.attr('id').replace(regex, repVal));
                        $item.attr('name', $item.attr('name').replace(regex, repVal));
                    });
                });
            }

            /**
             * Remove a form.
             */
            function removeForm() {
                var $removedForm = $(this).closest('.subform');
                var removedIndex = parseInt($removedForm.data('index'));

                $removedForm.remove();

                // Update indices
                adjustIndices(removedIndex);
            }

            /**
             * Add a new form.
             */
            function addForm(line) {
                //alert('#'+line+'-_-form'); //debug alert
                var $templateForm = $('#'+line+'-_-form'); // messy... This formats the passed function arg line into the templateForm var
                if ($templateForm.length === 0) {
                    console.log('[ERROR] Cannot find template');
                    return;
                }

                // Get Last index
                var $lastForm = $('.subform').last();

                var newIndex = 0;

                if ($lastForm.length > 0) {
                    newIndex = parseInt($lastForm.data('index')) + 1;
                }

                // Maximum of 20 subforms
                if (newIndex >= 20) {
                    console.log('[WARNING] Reached maximum number of elements');
                    return;
                }

                // Add elements
                var $newForm = $templateForm.clone();

                $newForm.attr('id', replaceTemplateIndex($newForm.attr('id'), newIndex));
                $newForm.data('index', newIndex);

                $newForm.find('label, input, select, textarea').each(function(idx) {
                    var $item = $(this);

                    if ($item.is('label')) {
                        // Update labels
                        $item.attr('for', replaceTemplateIndex($item.attr('for'), newIndex));
                        return;
                    }

                    // Update other fields
                    $item.attr('id', replaceTemplateIndex($item.attr('id'), newIndex));
                    $item.attr('name', replaceTemplateIndex($item.attr('name'), newIndex));
                });

                // Append
                $('#subforms-container').append($newForm);
                $newForm.addClass('subform');
                $newForm.removeClass('is-hidden');

                $newForm.find('.btn-close').click(removeForm);
                $newForm.find('.remove').click(removeForm);

            }


            $(document).ready(function() {
                $('#add').click(addForm);
                $('.remove').click(removeForm);

            });



// below function will get generate command GetSelectedText field and create a form with GetSelectedText as argument
			function GetSelectedText(){
				var e = document.getElementById("command-select");
				var result = e.options[e.selectedIndex].value;
                addForm(result)


			}