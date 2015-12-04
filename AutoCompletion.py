import sublime, sublime_plugin

class AutoCompletionCommand(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # print(prefix)

        snippets = []
        regions = []

        if len(prefix) < 1:
            return snippets
        else:
            regions = view.find_all('[^\w-]' + prefix + '[\w-]*', sublime.IGNORECASE)

        strs = []

        for r in regions:
            s = view.substr(r)[1:]
            if s not in strs and s != prefix:
                # print('---分割线1---')
                # print(s)
                strs.append(s)

        # print('---分割线2---')

        for x in strs:
            snippets += [(x + '(AutoCompletion)', x)]

        # print(snippets)

        return snippets
