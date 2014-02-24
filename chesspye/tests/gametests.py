'''
Created on Jun 22, 2013

@author: nick
'''
import unittest

from chesspye.game.games import VanillaChess
from chesspye.board.pieces import Pawn, Knight, Bishop, Rook, Queen, King, colors, piece_types

class TestPieceMovement(unittest.TestCase):

    def setUp(self):
        self.game = VanillaChess(None,None)
        self.game.board.clear_board()

    def tearDown(self):
        pass
    
    def testMoveNullPiece(self):
        self.assertFalse(self.game.rules.move_piece((0,0), (0,1), self.game.board), 'Cannot move NoneType piece')
    
    def testNormalPawnMoveWhite(self):
        self.game.board.pieces[(1,3)] = Pawn(colors.WHITE, times_moved=1)
        
        self.assertFalse(self.game.rules.move_piece((1,3), (3,3), self.game.board), 'Pawn moved two squares after already moving')
        self.assertTrue(self.game.rules.move_piece((1,3), (2,3), self.game.board), 'Pawn should be able to move one square')
    
    def testDoublePawnMoveWhite(self):
        self.game.board.pieces[(1,3)] = Pawn(colors.WHITE)
        
        self.assertFalse(self.game.board.pieces[(1,3)].has_moved(), 'Piece has not moved')
        self.assertTrue(self.game.rules.move_piece((1,3), (3,3), self.game.board), 'Pawn has not moved; two square move is possible')
        self.assertTrue(self.game.rules.move_piece((3,3), (4,3), self.game.board), 'Pawn should be able to move one square')
        self.assertFalse(self.game.rules.move_piece((4,3), (6,3), self.game.board), 'Pawn should not move two squares')
        
    def testNormalPawnMoveBlack(self):
        self.game.board.set_square_to_piece('e6', Pawn(colors.BLACK, times_moved=1))
        
        self.assertFalse(self.game.rules.move_piece('e6', 'e4', self.game.board), 'Pawn moved two squares after already moving')
        self.assertTrue(self.game.rules.move_piece('e6', 'e5', self.game.board), 'Pawn should be able to move one square')
    
    def testDoublePawnMoveBlack(self):
        self.game.board.set_square_to_piece('e7', Pawn(colors.BLACK))
        
        self.assertFalse(self.game.board.pieces[self.game.board.algebraic_to_coordinate_square('e7')].has_moved(), 'Piece has not moved')
        self.assertTrue(self.game.rules.move_piece('e7', 'e5', self.game.board), 'Pawn has not moved; two square move is possible')
        self.assertTrue(self.game.rules.move_piece('e5', 'e4', self.game.board), 'Pawn should be able to move one square')
        self.assertFalse(self.game.rules.move_piece('e4', 'e2', self.game.board), 'Pawn should not move two squares')
        
    def testPawnCannotMoveThreeSpaces(self):
        self.game.board.pieces[(1,3)] = Pawn(colors.WHITE)
        
        self.assertFalse(self.game.rules.move_piece((4,3), (7,3), self.game.board), 'Pawn should not move three squares')

    def testPawnCaptureWhite(self):
        self.game.board.pieces[(1,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,4)] = Pawn(colors.BLACK)
        self.game.board.pieces[(3,3)] = Pawn(colors.BLACK)
        
        self.assertTrue(self.game.rules.move_piece((1,3), (2,4), self.game.board), 'Pawn may capture to the right')
        self.assertTrue(self.game.rules.move_piece((2,4), (3,3), self.game.board), 'Pawn may capture to the left')
        
    def testPawnCaptureBlack(self):
        self.game.board.set_square_to_piece('d5', Pawn(colors.BLACK))
        self.game.board.set_square_to_piece('c4', Pawn(colors.WHITE))
        self.game.board.set_square_to_piece('d3', Pawn(colors.WHITE))
        
        self.assertTrue(self.game.rules.move_piece('d5', 'c4', self.game.board), 'Pawn may capture to the left')
        self.assertTrue(self.game.rules.move_piece('c4', 'd3', self.game.board), 'Pawn may capture to the right')
    
    def testPawnCannotCaptureOwnPiece(self):
        self.game.board.pieces[(1,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,2)] = Pawn(colors.WHITE)
        
        self.assertFalse(self.game.rules.move_piece((1,3), (2,4), self.game.board), 'Pawn cannot capture to the right')
        self.assertFalse(self.game.rules.move_piece((1,3), (2,2), self.game.board), 'Pawn cannot capture to the left')
    
    def testPawnIsBlockedByEnemy(self):
        self.game.board.pieces[(1,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,3)] = Pawn(colors.BLACK)
        
        self.assertFalse(self.game.rules.move_piece((1,3), (3,3), self.game.board), 'Pawn is blocked')
        
    def testPawnIsBlockedByAlly(self):
        self.game.board.pieces[(1,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,3)] = Pawn(colors.WHITE)
        
        self.assertFalse(self.game.rules.move_piece((1,3), (3,3), self.game.board), 'Pawn is blocked')
        
    def testEnPassentToLeft(self):
        self.skipTest('Not implemented')
        
    def testEnPassentToRight(self):
        self.skipTest('Not implemented')
        
    def testCannotEnPassentAfterMoreThanOneTurn(self):
        self.skipTest('Not implemented')
        
    def testCannotEnPassentPawnThatHasMovedTwoSpacesOneAtATime(self):
        self.skipTest('Not implemented')
        
    def testCannotEnPassentNonPawn(self):
        self.skipTest('Not implemented')
        
    def testCannotEnPassentOwnPiece(self):
        self.skipTest('Not implemented')
        
    def testCannotAttackEmptySquare(self):
        self.skipTest('Not implemented')
        
    def testKnightCanJump(self):
        self.game.board.pieces[(3,3)] = Knight(colors.WHITE)
        self.game.board.pieces[(2,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(3,2)] = Pawn(colors.WHITE)
        self.game.board.pieces[(3,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,2)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,2)] = Pawn(colors.WHITE)
        
        self.assertTrue(self.game.rules.move_piece((3,3), (5,4), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((5,4), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (5,2), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((5,2), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (1,4), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((1,4), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (1,2), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((1,2), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (4,5), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((4,5), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (2,5), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((2,5), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (4,1), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((4,1), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (2,1), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((2,1), (3,3), self.game.board), 'Knight may jump over blockers')
    
    def testKnightCapture(self):
        self.game.board.pieces[(3,3)] = Knight(colors.WHITE)
        self.game.board.pieces[(5,4)] = Pawn(colors.BLACK)
        self.game.board.pieces[(5,2)] = Pawn(colors.BLACK)
        self.game.board.pieces[(1,4)] = Pawn(colors.BLACK)
        self.game.board.pieces[(1,2)] = Pawn(colors.BLACK)
        self.game.board.pieces[(4,5)] = Pawn(colors.BLACK)
        self.game.board.pieces[(2,5)] = Pawn(colors.BLACK)
        self.game.board.pieces[(4,1)] = Pawn(colors.BLACK)
        self.game.board.pieces[(2,1)] = Pawn(colors.BLACK)
        
        self.assertTrue(self.game.rules.move_piece((3,3), (5,4), self.game.board), 'Knight may capture')
        self.assertTrue(self.game.rules.move_piece((5,4), (3,3), self.game.board), 'Knight may move to empty space')
        self.assertTrue(self.game.rules.move_piece((3,3), (5,2), self.game.board), 'Knight may capture')
        self.assertTrue(self.game.rules.move_piece((5,2), (3,3), self.game.board), 'Knight may move to empty space')
        self.assertTrue(self.game.rules.move_piece((3,3), (1,4), self.game.board), 'Knight may capture')
        self.assertTrue(self.game.rules.move_piece((1,4), (3,3), self.game.board), 'Knight may move to empty space')
        self.assertTrue(self.game.rules.move_piece((3,3), (1,2), self.game.board), 'Knight may capture')
        self.assertTrue(self.game.rules.move_piece((1,2), (3,3), self.game.board), 'Knight may move to empty space')
        self.assertTrue(self.game.rules.move_piece((3,3), (4,5), self.game.board), 'Knight may capture')
        self.assertTrue(self.game.rules.move_piece((4,5), (3,3), self.game.board), 'Knight may move to empty space')
        self.assertTrue(self.game.rules.move_piece((3,3), (2,5), self.game.board), 'Knight may capture')
        self.assertTrue(self.game.rules.move_piece((2,5), (3,3), self.game.board), 'Knight may move to empty space')
        self.assertTrue(self.game.rules.move_piece((3,3), (4,1), self.game.board), 'Knight may capture')
        self.assertTrue(self.game.rules.move_piece((4,1), (3,3), self.game.board), 'Knight may move to empty space')
        self.assertTrue(self.game.rules.move_piece((3,3), (2,1), self.game.board), 'Knight may capture')
        self.assertTrue(self.game.rules.move_piece((2,1), (3,3), self.game.board), 'Knight may move to empty space')
    
    def testKnightJumpAndCapture(self):
        self.game.board.pieces[(3,3)] = Knight(colors.WHITE)
        self.game.board.pieces[(2,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(3,2)] = Pawn(colors.WHITE)
        self.game.board.pieces[(3,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,2)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,2)] = Pawn(colors.WHITE)
        self.game.board.pieces[(5,4)] = Pawn(colors.BLACK)
        self.game.board.pieces[(5,2)] = Pawn(colors.BLACK)
        self.game.board.pieces[(1,4)] = Pawn(colors.BLACK)
        self.game.board.pieces[(1,2)] = Pawn(colors.BLACK)
        self.game.board.pieces[(4,5)] = Pawn(colors.BLACK)
        self.game.board.pieces[(2,5)] = Pawn(colors.BLACK)
        self.game.board.pieces[(4,1)] = Pawn(colors.BLACK)
        self.game.board.pieces[(2,1)] = Pawn(colors.BLACK)
        
        self.assertTrue(self.game.rules.move_piece((3,3), (5,4), self.game.board), 'Knight may jump over blockers to capture')
        self.assertTrue(self.game.rules.move_piece((5,4), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (5,2), self.game.board), 'Knight may jump over blockers to capture')
        self.assertTrue(self.game.rules.move_piece((5,2), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (1,4), self.game.board), 'Knight may jump over blockers to capture')
        self.assertTrue(self.game.rules.move_piece((1,4), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (1,2), self.game.board), 'Knight may jump over blockers to capture')
        self.assertTrue(self.game.rules.move_piece((1,2), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (4,5), self.game.board), 'Knight may jump over blockers to capture')
        self.assertTrue(self.game.rules.move_piece((4,5), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (2,5), self.game.board), 'Knight may jump over blockers to capture')
        self.assertTrue(self.game.rules.move_piece((2,5), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (4,1), self.game.board), 'Knight may jump over blockers to capture')
        self.assertTrue(self.game.rules.move_piece((4,1), (3,3), self.game.board), 'Knight may jump over blockers')
        self.assertTrue(self.game.rules.move_piece((3,3), (2,1), self.game.board), 'Knight may jump over blockers to capture')
        self.assertTrue(self.game.rules.move_piece((2,1), (3,3), self.game.board), 'Knight may jump over blockers')
        
    def testRookMovementOnEmptyBoard(self):
        self.game.board.pieces[(3,3)] = Rook(colors.WHITE)
        
        self.assertTrue(self.game.rules.move_piece((3,3), (3,4), self.game.board), 'Rook can move right one square')
        self.assertTrue(self.game.rules.move_piece((3,4), (3,7), self.game.board), 'Rook can move right more than one square')
        self.assertTrue(self.game.rules.move_piece((3,7), (3,1), self.game.board), 'Rook can move left more than one square')
        self.assertTrue(self.game.rules.move_piece((3,1), (3,0), self.game.board), 'Rook can move left one square')
        self.assertTrue(self.game.rules.move_piece((3,0), (4,0), self.game.board), 'Rook can move up one square')
        self.assertTrue(self.game.rules.move_piece((4,0), (7,0), self.game.board), 'Rook can move up more than one square')
        self.assertTrue(self.game.rules.move_piece((7,0), (1,0), self.game.board), 'Rook can move down more than one square')
        self.assertTrue(self.game.rules.move_piece((1,0), (0,0), self.game.board), 'Rook can move down one square')
        self.assertFalse(self.game.rules.move_piece((0,0), (2,2), self.game.board), 'Rook cannot move diagonally')
        
    def testRookCapture(self):
        self.game.board.pieces[(3,3)] = Rook(colors.WHITE)
        self.game.board.pieces[(3,4)] = Pawn(colors.BLACK)
        self.game.board.pieces[(3,7)] = Pawn(colors.BLACK)
        self.game.board.pieces[(3,1)] = Pawn(colors.BLACK)
        self.game.board.pieces[(3,0)] = Pawn(colors.BLACK)
        self.game.board.pieces[(4,0)] = Pawn(colors.BLACK)
        self.game.board.pieces[(7,0)] = Pawn(colors.BLACK)
        self.game.board.pieces[(1,0)] = Pawn(colors.BLACK)
        self.game.board.pieces[(0,0)] = Pawn(colors.BLACK)
        
        self.assertTrue(self.game.rules.move_piece((3,3), (3,4), self.game.board), 'Rook can move right one square')
        self.assertTrue(self.game.rules.move_piece((3,4), (3,7), self.game.board), 'Rook can move right more than one square')
        self.assertTrue(self.game.rules.move_piece((3,7), (3,1), self.game.board), 'Rook can move left more than one square')
        self.assertTrue(self.game.rules.move_piece((3,1), (3,0), self.game.board), 'Rook can move left one square')
        self.assertTrue(self.game.rules.move_piece((3,0), (4,0), self.game.board), 'Rook can move up one square')
        self.assertTrue(self.game.rules.move_piece((4,0), (7,0), self.game.board), 'Rook can move up more than one square')
        self.assertTrue(self.game.rules.move_piece((7,0), (1,0), self.game.board), 'Rook can move down more than one square')
        self.assertTrue(self.game.rules.move_piece((1,0), (0,0), self.game.board), 'Rook can move down one square')
        
    def testRookBeingBlocked(self):
        self.game.board.pieces[(3,3)] = Rook(colors.WHITE)
        self.game.board.pieces[(2,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(3,2)] = Pawn(colors.WHITE)
        self.game.board.pieces[(3,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,2)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,2)] = Pawn(colors.WHITE)
        
        self.assertFalse(self.game.rules.move_piece((3,3), (3,4), self.game.board), 'Rook cannot move right one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (3,7), self.game.board), 'Rook cannot move right more than one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (3,2), self.game.board), 'Rook cannot move left one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (3,0), self.game.board), 'Rook cannot move left more than one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (4,3), self.game.board), 'Rook cannot move up one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (7,3), self.game.board), 'Rook cannot move up more than one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (2,3), self.game.board), 'Rook cannot move down one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (0,3), self.game.board), 'Rook cannot move down more than one square')
        
    def testBishopMovementOnEmptyBoard(self):
        self.game.board.pieces[(3,3)] = Bishop(colors.WHITE)
        
        self.assertTrue(self.game.rules.move_piece((3,3), (4,4), self.game.board), 'Bishop can move up right one square')
        self.assertTrue(self.game.rules.move_piece((4,4), (7,7), self.game.board), 'Bishop can move up right more than one square')
        self.assertTrue(self.game.rules.move_piece((7,7), (6,6), self.game.board), 'Bishop can move down left one square')
        self.assertTrue(self.game.rules.move_piece((6,6), (3,3), self.game.board), 'Bishop can move down left more than one square')
        self.assertTrue(self.game.rules.move_piece((3,3), (2,4), self.game.board), 'Bishop can move up left one square')
        self.assertTrue(self.game.rules.move_piece((2,4), (0,6), self.game.board), 'Bishop can move up left more than one square')
        self.assertTrue(self.game.rules.move_piece((0,6), (1,5), self.game.board), 'Bishop can move down right one square')
        self.assertTrue(self.game.rules.move_piece((1,5), (5,1), self.game.board), 'Bishop can move down right more than one square')
        self.assertFalse(self.game.rules.move_piece((1,5), (2,5), self.game.board), 'Bishop cannot move linearly')
    
    def testBishopCapture(self):
        self.game.board.pieces[(3,3)] = Bishop(colors.WHITE)
        self.game.board.pieces[(4,4)] = Pawn(colors.BLACK)
        self.game.board.pieces[(7,7)] = Pawn(colors.BLACK)
        self.game.board.pieces[(2,4)] = Pawn(colors.BLACK)
        self.game.board.pieces[(0,6)] = Pawn(colors.BLACK)
        self.game.board.pieces[(5,1)] = Pawn(colors.BLACK)
        
        self.assertTrue(self.game.rules.move_piece((3,3), (4,4), self.game.board), 'Bishop can move up right one square')
        self.assertTrue(self.game.rules.move_piece((4,4), (7,7), self.game.board), 'Bishop can move up right more than one square')
        self.assertTrue(self.game.rules.move_piece((7,7), (6,6), self.game.board), 'Bishop can move down left one square')
        self.assertTrue(self.game.rules.move_piece((6,6), (3,3), self.game.board), 'Bishop can move down left more than one square')
        self.assertTrue(self.game.rules.move_piece((3,3), (2,4), self.game.board), 'Bishop can move up left one square')
        self.assertTrue(self.game.rules.move_piece((2,4), (0,6), self.game.board), 'Bishop can move up left more than one square')
        self.assertTrue(self.game.rules.move_piece((0,6), (1,5), self.game.board), 'Bishop can move down right one square')
        self.assertTrue(self.game.rules.move_piece((1,5), (5,1), self.game.board), 'Bishop can move down right more than one square')
    
    def testBishopBeingBlocked(self):
        self.game.board.pieces[(3,3)] = Bishop(colors.WHITE)
        self.game.board.pieces[(2,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,3)] = Pawn(colors.WHITE)
        self.game.board.pieces[(3,2)] = Pawn(colors.WHITE)
        self.game.board.pieces[(3,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,2)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(2,4)] = Pawn(colors.WHITE)
        self.game.board.pieces[(4,2)] = Pawn(colors.WHITE)
        
        self.assertFalse(self.game.rules.move_piece((3,3), (4,4), self.game.board), 'Bishop cannot move up right one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (7,7), self.game.board), 'Bishop cannot move up right more than one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (2,2), self.game.board), 'Bishop cannot move down left one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (0,0), self.game.board), 'Bishop cannot move down left more than one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (2,4), self.game.board), 'Bishop cannot move up left one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (0,6), self.game.board), 'Bishop cannot move up left more than one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (4,2), self.game.board), 'Bishop cannot move down right one square')
        self.assertFalse(self.game.rules.move_piece((3,3), (6,0), self.game.board), 'Bishop cannot move down right more than one square')
    
    def testCanKingSideCastle(self):
        self.game.board.set_square_to_piece('h1', Rook(colors.WHITE))
        self.game.board.set_square_to_piece('e1', King(colors.WHITE))
        
        self.assertTrue(self.game.rules.move_piece('e1', 'g1', self.game.board), 'King should be able to castle')
        self.assertEqual(self.game.board.get_square('h1'), None, 'h1 should be NoneType but is %s' % self.game.board.get_square('h1'))
        self.assertTrue(self.game.board.get_square('g1').piece_type == piece_types.KING, 'Piece on g1 should be a King')
        self.assertTrue(self.game.board.get_square('f1').piece_type == piece_types.ROOK, 'Piece on f1 should be a Rook')
        
    def testCanQueenSideCastle(self):
        self.game.board.set_square_to_piece('a1', Rook(colors.WHITE))
        self.game.board.set_square_to_piece('e1', King(colors.WHITE))
        
        self.assertTrue(self.game.rules.move_piece('e1', 'c1', self.game.board), 'King should be able to castle')
        self.assertEqual(self.game.board.get_square('a1'), None, 'a1 should be NoneType but is %s' % self.game.board.get_square('h1'))
        self.assertTrue(self.game.board.get_square('c1').piece_type == piece_types.KING, 'Piece on g1 should be a King')
        self.assertTrue(self.game.board.get_square('d1').piece_type == piece_types.ROOK, 'Piece on f1 should be a Rook')
        
    def testCannotCastleWhenPiecesBlocking(self):
        self.game.board.set_square_to_piece('a1', Rook(colors.WHITE))
        self.game.board.set_square_to_piece('h1', Rook(colors.WHITE))
        self.game.board.set_square_to_piece('e1', King(colors.WHITE))
        self.game.board.set_square_to_piece('d1', Queen(colors.WHITE))
        self.game.board.set_square_to_piece('f1', Bishop(colors.WHITE))
        
        self.assertFalse(self.game.rules.move_piece('e1', 'g1', self.game.board), 'King should not be able to king side castle')
        self.assertFalse(self.game.rules.move_piece('e1', 'c1', self.game.board), 'King should not be able to queen side castle')
        
        self.assertTrue(self.game.board.get_square('e1').piece_type == piece_types.KING, 'Piece on g1 should be a King')
        self.assertTrue(self.game.board.get_square('a1').piece_type == piece_types.ROOK, 'Piece on a1 should be a Rook')
        self.assertTrue(self.game.board.get_square('h1').piece_type == piece_types.ROOK, 'Piece on h1 should be a Rook')
        self.assertTrue(self.game.board.get_square('d1').piece_type == piece_types.QUEEN, 'Piece on d1 should be a Queen')
        self.assertTrue(self.game.board.get_square('f1').piece_type == piece_types.BISHOP, 'Piece on f1 should be a Bishop')
        
    def testCannotCastleWhenKingHasMoved(self):
        self.game.board.set_square_to_piece('a1', Rook(colors.WHITE, times_moved=1))
        self.game.board.set_square_to_piece('h1', Rook(colors.WHITE, times_moved=1))
        self.game.board.set_square_to_piece('e1', King(colors.WHITE))
        
        self.assertFalse(self.game.rules.move_piece('e1', 'g1', self.game.board), 'King should not be able to king side castle')
        self.assertFalse(self.game.rules.move_piece('e1', 'c1', self.game.board), 'King should not be able to queen side castle')
        
    def testCannotCastleWhenRooksHaveMoved(self):
        self.game.board.set_square_to_piece('a1', Rook(colors.WHITE))
        self.game.board.set_square_to_piece('h1', Rook(colors.WHITE))
        self.game.board.set_square_to_piece('e1', King(colors.WHITE, times_moved=1))
        
        self.assertFalse(self.game.rules.move_piece('e1', 'g1', self.game.board), 'King should not be able to king side castle')
        self.assertFalse(self.game.rules.move_piece('e1', 'c1', self.game.board), 'King should not be able to queen side castle')
        
    def testKingCannotMoveTwoSquaresNormally(self):
        self.game.board.set_square_to_piece('e4', King(colors.WHITE))
        
        self.assertFalse(self.game.rules.move_piece('e4', 'g4', self.game.board), 'King should not be able to move 2 squares')
        self.assertFalse(self.game.rules.move_piece('e4', 'c4', self.game.board), 'King should not be able to move 2 squares')
        
    def testKingCannotMoveTwoSquaresNormallyFromHomeSquare(self):
        self.game.board.set_square_to_piece('e1', King(colors.WHITE))
        
        self.assertFalse(self.game.rules.move_piece('e1', 'g1', self.game.board), 'King should not be able to move 2 squares')
        self.assertFalse(self.game.rules.move_piece('e1', 'c1', self.game.board), 'King should not be able to move 2 squares')

if __name__ == "__main__":
    unittest.main()