/* Copyright (C) 2014, Jill Huchital
*/

function fillTool() {
    do_api_call('get_all_categories', {}, function(category_data) {
        var cur_category, cur_arc, i, j, k, t, cur_topic,
            search_term_string, category_dom_content, category_name_content, tmp,
            tablerow_dom_content, arcpos_name, arcpos_search, arcpos_button,
            topic_name, topic_search, add_topic_button, buttonclickhelper;

        buttonclickhelper = function(category) {
            return function(e) {
                var formElement = this.parentNode, i,
                    new_topic_name = formElement.querySelector('input[name="topic_display_name"]').value,
                    new_search_term_string = formElement.querySelector('input[name="topic_search_terms"]').value,
                    new_search_terms = [],
                    params = {};
                if (new_topic_name === '') {
                    alert('Please name the new topic');
                    return;
                }
                if (new_search_term_string === '') {
                    alert('Please provide search terms');
                    return;
                }
                new_search_terms = new_search_term_string.split(',');
                for (i=0;i<new_search_terms.length;i+=1) {
                    new_search_terms[i] = new_search_terms[i].trim();
                }
                params = {'category_name': category,
                    'topic_name': new_topic_name,
                    'search_terms': new_search_terms};
                do_api_call('add_topic', params, function(retval) {
                        console.log('seems OK');
                    }, function(error_string) {
                        console.log(error_string);
                });
            }
        }

        for (i=0;i<category_data['all_categories'].length;i+=1) {
            cur_category = category_data['all_categories'][i];
            arcstring = cur_category['arc'][0]['arcpos']
            /* clone the category template, put it in the DOM */

            tmp = document.querySelector('#category_template').content;
            category_dom_content = document.importNode(tmp, true);
            category_name_content = category_dom_content.querySelector('.category_name');
            category_name_content.textContent = cur_category['category_name'];

            /* for each arcpos, make a table row */
            for (j=0;j<cur_category['arc'].length;j+=1) {
                cur_arc = cur_category['arc'][j];
                tablerow_dom_content = document.querySelector('.arcpos_tablerow_template').content;
                arcpos_name = tablerow_dom_content.querySelector('.arcpos_name');
                arcpos_search = tablerow_dom_content.querySelector('.arcpos_searchterms');
                arcpos_name.textContent = cur_arc['arcpos'];
                search_term_string = cur_arc['search_terms'][0];
                for (k=1;k<cur_arc['search_terms'].length;k+=1) {
                    search_term_string += ", "
                    search_term_string += cur_arc['search_terms'][k];
                }
                arcpos_search.textContent = search_term_string;
                category_dom_content.querySelector('.category_table').appendChild(
                        document.importNode(tablerow_dom_content, true));
            }
            /* for each topic, make a table row */
            for (t in cur_category['topic_data']) {
                cur_topic = cur_category['topic_data'][t];
                tablerow_dom_content = document.querySelector('.topic_tablerow_template').content;
                topic_name = tablerow_dom_content.querySelector('.topic_display_name');
                topic_search = tablerow_dom_content.querySelector('.topic_searchterms');
                topic_name.textContent = cur_topic['topic_display_name'];
                search_term_string = cur_topic['search_terms'][0];
                for (k=1;k<cur_topic['search_terms'].length;k+=1) {
                    search_term_string += ", "
                    search_term_string += cur_topic['search_terms'][k];
                }
                topic_search.textContent = search_term_string;
                category_dom_content.querySelector('.topic_table').appendChild(
                        document.importNode(tablerow_dom_content, true));
            }
            /* set the click handler for the "add topic" button */
            add_topic_button = category_dom_content.querySelector('.add_topic_button');
            add_topic_button.onclick = buttonclickhelper(cur_category['category_name']);
            document.querySelector('#arcs').appendChild(category_dom_content);
        }
    }, function(error_string) {
        console.log(error_string);
    });
}
