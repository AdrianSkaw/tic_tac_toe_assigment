def route(app, controller):
    app.add_url_rule('/api/new_session/<player>', 'new_session', controller.new_session, methods=['POST'])
    app.add_url_rule('/api/start_game/<player>', 'start_game', controller.start_game, methods=['POST'])
    app.add_url_rule('/api/add_credits/<player>', 'add_credits', controller.add_credits, methods=['POST'])
    app.add_url_rule('/api/move/<id>/<player>', 'move', controller.make_move, methods=['POST']),
    app.add_url_rule('/api/board/<id_>', 'board', controller.get_board, methods=['GET'])
    app.add_url_rule('/api/credits/<player>', 'credits', controller.get_credits, methods=['GET'])
    app.add_url_rule('/api/end_session/<player>', 'end_session', controller.end_session, methods=['POST'])
    app.add_url_rule('/api/get_stats', 'get_stats', controller.get_stats, methods=['GET'])
