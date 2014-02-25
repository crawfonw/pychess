'''
Created on Feb 22, 2014

@author: Nick Crawford

Note on the move_rules dict:
    Each rule method must consume (from_sq, to_sq, move_vector, piece, board):
        piece - instance of a Piece
        from_sq, to_sq - each a tuple of coordinates of starting and ending pos
        move_vector - computed via from_sq and to_sq in main move handling method
        board - the current board state of the game
        move_stack - Stack obj containing all the previous moves
    
    If more rules are added (i.e. for variants) they must be in the extended
    rules class if you want them to interact with game_variables (duh)
'''

from chesspye.board.pieces import colors, move_types, piece_types
from chesspye.utils import Vec2d

from copy import deepcopy
from math import copysign

class Rules(object):
    
    def __init__(self):
        self.move_rules = {} #These are all checked every move
        self.move_actions = {} #These are executed when a specific move rule applies (actually move the pieces)
        self.game_variables = {}
        
    def register_move_rule(self, f, name=None):
        if name is None:
            self.move_rules[f.__name__] = f
        else:
            self.move_rules[name] = f
            
    def register_move_action(self, f, name=None):
        if name is None:
            self.move_actions[f.__name__] = f
        else:
            self.move_actions[name] = f
            
    def register_game_variable(self, name, val):
        self.game_variables[name] = val

class VanillaRules(Rules):

    def __init__(self):
        super(VanillaRules, self).__init__()
        self.register_game_variable('white_can_kingside_castle', True)
        self.register_game_variable('white_can_queenside_castle', True)
        self.register_game_variable('black_can_kingside_castle', True)
        self.register_game_variable('black_can_queenside_castle', True)
        self.register_game_variable('fifty_move_counter', 0)
        
        self.register_move_rule(self.generic_move_rule, 'generic_move_rule')
        self.register_move_action(self.handle_generic_move, 'generic')
        
        self.register_move_rule(self.en_passante_rule, 'en_passante_rule')
        self.register_move_action(self.handle_en_passante, 'en_passante')
        
        self.register_move_rule(self.castle_rule, 'castle_rule')
        self.register_move_action(self.handle_castle, 'castle')
    
    #Methods to call from Game instance    
    def move_piece(self, from_sq, to_sq, board):
        if type(from_sq) == type(to_sq):
            if type(from_sq) == tuple:
                if self.move_piece_coordinate(from_sq, to_sq, board):
                    board.moves.push((board.pieces[to_sq], from_sq, to_sq))
                    return True
                return False
            elif type(from_sq) == str:
                from_sq = board.algebraic_to_coordinate_square(from_sq)
                to_sq = board.algebraic_to_coordinate_square(to_sq)
                if self.move_piece_coordinate(from_sq, to_sq, board):
                    board.moves.push((board.pieces[to_sq], from_sq, to_sq))
                    return True
                return False
            else:
                raise TypeError("Invalid square specification data type %s" % type(from_sq))
        else:
            raise TypeError("from_sq and to_sq datatypes must match! (Inputs were %s and %s.)" % (type(from_sq), type(to_sq)))
    
    def move_piece_algebraic(self, from_sq, to_sq, board):
        #i.e. d1-d4 not Qd4
        return self.move_piece_coordinate(board.algebraic_to_coordinate_square(from_sq), \
                          board.algebraic_to_coordinate_square(to_sq), board)

    def move_piece_coordinate(self, from_sq, to_sq, board):
        valid = self.is_valid_move(from_sq, to_sq, board) 
        if valid is not None:
            return self.do_move(valid['name'], valid, board)
        else:
            return False
    
    #Movement/board state validators
    def is_valid_move(self, from_sq, to_sq, board):
        if from_sq == to_sq:
            return None
        if not board.square_is_on_board(from_sq):
            return None
        
        #if piece.piece_type == piece_types.KING:
        #    if self.is_square_guarded_by(to_sq, piece.color * -1, board):
        #        return False
        
        piece = board.pieces[from_sq]
        if piece is not None:
            move_vector = Vec2d(to_sq) - Vec2d(from_sq)
            for name, rule in self.move_rules.items():
                rule_to_apply = rule(from_sq, to_sq, move_vector, piece, board) 
                if rule_to_apply:
                    break
        
            #At this point, all the rules passed, so let's make the move on a dummy board
            #and test if we got ourselves in check
            board_copy = None
            if self.king_is_in_check(piece.color, board):
                return None
            return rule_to_apply
        return None
    
    def is_square_guarded_by(self, square, color, board):
        colored_pieces = []
        for loc, piece in board.pieces.items():
            if piece is not None:
                if piece.color == color:
                    colored_pieces.append((loc, piece))
        for loc, piece in colored_pieces:
            move_vector = Vec2d(loc) - Vec2d(square)
            if self.generic_move_rule(loc, square, move_vector, piece, board):
                return True
        return False
    
    def king_is_in_check(self, color, board):
        if board.kings[color] is None: #for testing or variants
            return False
        return self.is_square_guarded_by(board.kings[color], color * -1, board)

    #Movement rules
    def generic_move_rule(self, from_sq, to_sq, move_vector, piece, board):
        pattern_types = None
        to_sq_piece = board.pieces[to_sq]
        if to_sq_piece is not None:
            if piece.color == to_sq_piece.color:
                return None
            else:
                pattern_types = piece.attack_patterns()
        else:
            pattern_types = piece.move_patterns()
        
        if piece.move_type == move_types.EXACT:
            #The following logic might not work for weird moving piece_types
            #(i.e. Knight) if they cannot jump
            #TODO: verify/fix this
            for move in pattern_types:
                if Vec2d(move) + Vec2d(from_sq) == Vec2d(to_sq):
                    if piece.can_jump:
                        return {'name':'generic', 'from_sq':from_sq, 'to_sq':to_sq}
                    else:
                        #This piece can move here assuming it is unblocked
                        #Now find the straight-line path and make sure nothing is blocking
                        f = lambda x : int(copysign(1,x)) if x != 0 else 0
                        unit_move = Vec2d(f(move[0]), f(move[1])) #unit vector in direction of move
                        curr_sq = Vec2d(from_sq) + unit_move
                        while tuple(curr_sq) != to_sq:
                            if not board.square_is_on_board(tuple(curr_sq)):
                                return None
                            if board.pieces[tuple(curr_sq)] is not None:
                                return None
                            curr_sq += unit_move
                        return {'name':'generic', 'from_sq':from_sq, 'to_sq':to_sq}
        elif piece.move_type == move_types.MAX:
            for move in pattern_types:
                dir_vec = Vec2d(move) #a unit vector
                #This direction is a valid movement if vectorized coordinates 
                #have an angle of zero between them and point the same direction
                #(i.e. scalar multiples of one another)
                if dir_vec.get_angle_between(move_vector) == 0:
                    curr_sq = Vec2d(from_sq) + dir_vec
                    while tuple(curr_sq) != to_sq:
                        if not board.square_is_on_board(tuple(curr_sq)):
                            return None
                        if board.pieces[tuple(curr_sq)] is not None and not piece.can_jump:
                            return None
                        curr_sq += dir_vec
                    return {'name':'generic', 'from_sq':from_sq, 'to_sq':to_sq}

    def en_passante_rule(self, from_sq, to_sq, move_vector, piece, board):
        if piece.piece_type == piece_types.PAWN and tuple(move_vector) in piece.attack_patterns():
            other_piece_sq = tuple(Vec2d(from_sq) + Vec2d(0, move_vector.y))
            other = board.pieces[other_piece_sq]
            if other is not None and other.piece_type == piece_types.PAWN and other.color != piece.color:
                last_move = board.moves.peek()
                if last_move is not None and other is last_move[0] and other.times_moved == 1: #Want the same exact piece (in memory)
                    return {'name': 'en_passante', 'from_sq':from_sq, \
                            'to_sq':to_sq, 'other_piece_sq':other_piece_sq}
                return None
            
    def castle_rule(self, from_sq, to_sq, move_vector, piece, board):
        if piece.piece_type == piece_types.KING and move_vector.get_length() == 2:
            if piece.has_moved():
                return None
            if piece.color == colors.WHITE:
                if self.game_variables['white_can_kingside_castle'] and move_vector == Vec2d(0,2):
                    if board.pieces[to_sq] is not None or board.pieces[tuple(Vec2d(to_sq) + Vec2d(0,-1))] is not None:
                        return None
                    rook_loc = tuple(Vec2d(to_sq) + Vec2d(0,1))
                    rook_dest = tuple(Vec2d(to_sq) + Vec2d(0,-1))
                elif self.game_variables['white_can_queenside_castle'] and move_vector == Vec2d(0,-2):
                    if board.pieces[to_sq] is not None or \
                        board.pieces[tuple(Vec2d(to_sq) + Vec2d(0,1))] is not None or \
                        board.pieces[tuple(Vec2d(to_sq) + Vec2d(0,-1))] is not None:
                        return None
                    rook_loc = tuple(Vec2d(to_sq) + Vec2d(0,-2))
                    rook_dest = tuple(Vec2d(to_sq) + Vec2d(0,1))
                else:
                    return None
            elif piece.color == colors.BLACK:
                if self.game_variables['black_can_kingside_castle'] and move_vector == Vec2d(0,2):
                    if board.pieces[to_sq] is not None or board.pieces[tuple(Vec2d(to_sq) + Vec2d(0,-1))] is not None:
                        return None
                    rook_loc = tuple(Vec2d(to_sq) + Vec2d(0,1))
                    rook_dest = tuple(Vec2d(to_sq) + Vec2d(0,-1))
                elif self.game_variables['black_can_queenside_castle'] and move_vector == Vec2d(0,-2):
                    if board.pieces[to_sq] is not None or \
                        board.pieces[tuple(Vec2d(to_sq) + Vec2d(0,1))] is not None or \
                        board.pieces[tuple(Vec2d(to_sq) + Vec2d(0,-1))] is not None:
                        return None
                    rook_loc = tuple(Vec2d(to_sq) + Vec2d(0,-2))
                    rook_dest = tuple(Vec2d(to_sq) + Vec2d(0,1))
                else:
                    return None
            
            if not board.square_is_on_board(rook_loc):
                return None
            rook = board.pieces[rook_loc]
            if rook is None or rook.piece_type != piece_types.ROOK or rook.has_moved():
                return None

            return {'name':'castle', 'from_sq':from_sq, 'to_sq':to_sq, 'rook_loc':rook_loc, \
                    'rook_dest':rook_dest}
            
    def do_move(self, action, data, board):
        return self.move_actions[action](data, board)
    
    def handle_generic_move(self, data, board):
        from_sq = data['from_sq']
        to_sq = data['to_sq']
        piece = board.pieces[from_sq]
        board.pieces[from_sq] = None
        board.pieces[to_sq] = piece
        
        if piece.piece_type == piece_types.KING:
            board.kings[piece.color] = to_sq
            if piece.color == colors.WHITE:
                self.game_variables['white_can_kingside_castle'] = False
                self.game_variables['white_can_queenside_castle'] = False
            elif piece.color == colors.BLACK:
                self.game_variables['black_can_kingside_castle'] = False
                self.game_variables['black_can_queenside_castle'] = False
        #Hard-coded
        #TODO: Un-hardcode rook locations for support for possible variants 
        elif piece.piece_type == piece_types.ROOK:
            if piece.color == colors.WHITE:
                if not piece.has_moved():
                    if from_sq == (0,7):
                        self.game_variables['white_can_kingside_castle'] = False
                    elif from_sq == (0,0):
                        self.game_variables['white_can_queenside_castle'] = False
                elif piece.color == colors.BLACK:
                    if not piece.has_moved():
                        if from_sq == (7,7):
                            self.game_variables['black_can_kingside_castle'] = False
                        elif from_sq == (7,0):
                            self.game_variables['black_can_queenside_castle'] = False
        
        piece.times_moved += 1
        return True
    
    def handle_castle(self, data, board):
        from_sq = data['from_sq']
        to_sq = data['to_sq']
        rook_loc = data['rook_loc']
        rook_dest = data['rook_dest']
        piece = board.pieces[from_sq]
        rook = board.pieces[rook_loc] 
        
        board.pieces[from_sq] = None
        board.pieces[to_sq] = piece
        piece.times_moved += 1
        
        board.pieces[rook_loc] = None
        board.pieces[rook_dest] = rook
        rook.times_moved += 1
        
        if piece.color == colors.WHITE:
            self.game_variables['white_can_kingside_castle'] = False
            self.game_variables['white_can_queenside_castle'] = False
        elif piece.color == colors.BLACK:
            self.game_variables['black_can_kingside_castle'] = False
            self.game_variables['black_can_queenside_castle'] = False
        return True
    
    def handle_en_passante(self, data, board):
        piece = board.pieces[data['from_sq']]
        board.pieces[data['other_piece_sq']] = None
        board.pieces[data['from_sq']] = None
        board.pieces[data['to_sq']] = piece
        piece.times_moved += 1
        return True