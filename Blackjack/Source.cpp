// Blackjack
// Plays a simple version of the casino card game for 1 - 7 players

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <ctime>

using namespace std;

// ****************************************************************************************************
class Card {
public:
	// Creating two enumerations to represent the value on a card and the suit on the card
	// This way the values aren't just number values, but readable words
	enum rank{ACE = 1, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING};
	enum suit{CLUBS, DIAMONDS, HEARTS, SPADES};
	// Overloading the << operator so I can send Card object to standard output
	friend ostream& operator<<(ostream& os, const Card& aCard);
	// Default values for the constructor
	Card(rank r = ACE, suit s = SPADES, bool ifu = true);
	// Returns the value of a card, 1 - 11
	int GetValue() const;
	// Flips a card; if face up, becomes face down and vice versa
	void Flip();
private:
	rank m_Rank;
	suit m_Suit;
	bool m_IsFaceUp;
};

Card::Card(rank r, suit s, bool ifu):
	m_Rank(r), m_Suit(s), m_IsFaceUp(ifu)
{}

int Card::GetValue() const {
	// If a card is facedown, its value is 0
	int value = 0;
	if (m_IsFaceUp)
	{
		// Value is number showing on card
		value = m_Rank;
		// Value is 10 for face cards
		if (value > 10)
		{
			value = 10;
		}
	}
	return value;
}

void Card::Flip() {
	m_IsFaceUp = !(m_IsFaceUp);
}

// ****************************************************************************************************
class Hand {
public:
	Hand();
	virtual ~Hand();
	// Adds a card to the hand
	void Add(Card* pCard);
	// Clears hand of all cards
	void Clear();
	// Gets hand total value, intelligently treats aces as 1 or 11
	int GetTotal() const;
protected:
	vector<Card*> m_Cards;
};

Hand::Hand() {
	m_Cards.reserve(7);
}

Hand::~Hand() {
	Clear();
}

void Hand::Add(Card* pCard) {
	m_Cards.push_back(pCard);
}

void Hand::Clear() {
	// Iterate through vector, freeing all memory on the heap
	vector<Card*>::iterator iter = m_Cards.begin();
	for (iter = m_Cards.begin(); iter != m_Cards.end(); ++iter)
	{
		delete* iter;
		*iter = 0;
	}
	// Clear vector of pointers
	m_Cards.clear();
}

int Hand::GetTotal() const {
	// If no cards in hand, return 0
	if (m_Cards.empty())
	{
		return 0;
	}
	// If a first card has a value of 0, then card is face down - return 0
	if (m_Cards[0]->GetValue() == 0)
	{
		return 0;
	}
	// Add up card values, each Ace is treated as 1
	int total = 0;
	vector<Card*>::const_iterator iter;
	for (iter = m_Cards.begin(); iter != m_Cards.end(); ++iter)
	{
		total += (*iter)->GetValue();
	}
	// Determine if hand has an Ace
	bool containsAce = false;
	for (iter = m_Cards.begin(); iter != m_Cards.end(); ++iter)
	{
		if ((*iter)->GetValue() == Card::ACE)
		{
			containsAce = true;
		}
	}
	// If hand contains ace and total is low enough, treat ace as 11
	if (containsAce && total <= 11)
	{
		// Add only 10 since we have already added 1 for the ace
		total += 10;
	}
	return total;
}

// ****************************************************************************************************
class GenericPlayer : public Hand {
	friend ostream& operator<<(ostream& os, const GenericPlayer& aGenericPlayer);
public:
	GenericPlayer(const string& name = "");
	virtual ~GenericPlayer();
	// Inidcates whether or not generic player wants to keep hitting
	virtual bool IsHitting() const = 0;
	// Returns whether generic player has busted (total over 21)
	bool IsBusted() const;
	// Announces that the generic player busts
	void Busts() const;
protected:
	string m_Name;
};

GenericPlayer::GenericPlayer(const string& name):
	m_Name(name)
{}

GenericPlayer::~GenericPlayer()
{}

bool GenericPlayer::IsBusted() const {
	return (GetTotal() > 21);
}

void GenericPlayer::Busts() const {
	cout << m_Name << " busts!\n";
}

// ****************************************************************************************************
class Player : public GenericPlayer
{
public:
	Player(const string& name = "");
	virtual ~Player();
	// Returns whether or not the player wants another hit
	virtual bool IsHitting() const;
	// Announces that the player wins
	void Win() const;
	// Announces that the player loses
	void Lose() const;
	// Announces that the player pushes
	void Push() const;
};

Player::Player(const string& name) :
	GenericPlayer(name)
{}

Player::~Player()
{}

bool Player::IsHitting() const {
	cout << m_Name << ", do you want to hit? (Y/N): ";
	char response;
	cin >> response;
	return (response == 'y' || response == 'Y');
}

void Player::Win() const {
	cout << m_Name << " wins.\n";
}

void Player::Lose() const {
	cout << m_Name << " loses.\n";
}

void Player::Push() const {
	cout << m_Name << " pushes.\n";
}

// ****************************************************************************************************
class House :public GenericPlayer
{
public:
	House(const string& name = "House");
	virtual ~House();

	// Indicates whether house is hitting - will always hit on 16 or less
	virtual bool IsHitting() const;
	// Flips over the first card
	void FlipFirstCard();
};

House::House(const string& name):
	GenericPlayer(name)
{}

House::~House()
{}

bool House::IsHitting() const {
	return (GetTotal() <= 16);
}

void House::FlipFirstCard()
{
	if (!(m_Cards.empty()))
	{
		m_Cards[0]->Flip();
	}
	else
	{
		cout << "No card to flip!\n";
	}
}

// ****************************************************************************************************
class Deck :public Hand
{
public:
	Deck();
	virtual ~Deck();
	// Create a standard deck of 52 cards
	void populate();
	// Shuffle cards
	void Shuffle();
	// Deal one card to each hand
	void Deal(Hand& aHand);
	// Give additional cards to generic player
	void AdditionalCards(GenericPlayer& aGenericPlayer);
};

Deck::Deck() {
	m_Cards.reserve(52);
	populate();
}

Deck::~Deck()
{}

// Nested loops to go through and create a card for each value within each suit
void Deck::populate() {
	Clear();
	// Create a standard deck
	for (int s = Card::CLUBS; s <= Card::SPADES; ++s)
	{
		for (int r = Card::ACE; r <= Card::KING; ++r)
		{
			// Using static_cast to return a value of a new type from a value of another type
			Add(new Card(static_cast<Card::rank>(r), static_cast<Card::suit>(s)));
		}
	}
}

// Randomly rearranges the pointers in m_Cards with random_shuffle() from template library <algorithm>
void Deck::Shuffle() {
	random_shuffle(m_Cards.begin(), m_Cards.end());
}

// Deals one card from the deck to a hand
// Adds a copy of the pointer to the back of m_Cards to the object through the Add() member function
// Then it removes the pointer at the back of m_Cards, effectively transfering the card from the
// deck into the hand
void Deck::Deal(Hand& aHand) {
	if (!m_Cards.empty())
	{
		aHand.Add(m_Cards.back());
		m_Cards.pop_back();
	}
	else
	{
		cout << "Out of cards. Unable to deal.";
	}
}

// This function gives additional cards to whichever player's turn it is until they stop hitting
// or they go bust, since it accepts reference to an abstract class it can be called on by any of
// the classes that are derived from GenericPlayer class
void Deck::AdditionalCards(GenericPlayer& aGenericPlayer)
{
	cout << endl;
	// Continue to deal a card as long as generic player isn't busted and wants another hit
	while (!(aGenericPlayer.IsBusted()) && aGenericPlayer.IsHitting())
	{
		Deal(aGenericPlayer);
		cout << aGenericPlayer << endl;

		if (aGenericPlayer.IsBusted())
		{
			aGenericPlayer.Busts();
		}
	}
}

// ****************************************************************************************************
class Game
{
public:
	Game(const vector<string>& names);
	~Game();
	// Plays the game of Blackjack
	void Play();
private:
	Deck m_deck;
	House m_house;
	vector<Player> m_Players;
};

// Constructor accepts a reference to a vector of string objects, which represents the names of
// human players
Game::Game(const vector<string>& names) {
	// Create a vector of players from a vector of names
	vector<string>::const_iterator pName;
	for (pName = names.begin(); pName != names.end(); ++pName)
	{
		m_Players.push_back(Player(*pName));
	}
	// Seeds the random number generator
	srand(static_cast<unsigned int > (time(0)));
	m_deck.populate();
	m_deck.Shuffle();
}

Game::~Game()
{}

void Game::Play() {
	// Deal the initial 2 cards to everyone
	vector<Player>::iterator pPlayer;
	for (int i = 0; i < 2; ++i)
	{
		for (pPlayer = m_Players.begin(); pPlayer != m_Players.end(); ++pPlayer)
		{
			m_deck.Deal(*pPlayer);
		}
		m_deck.Deal(m_house);
	}
	// Hide house's first card
	m_house.FlipFirstCard();
	// Display everyones' hands
	for (pPlayer = m_Players.begin(); pPlayer != m_Players.end(); ++pPlayer)
		{
			cout << *pPlayer << endl;
		}
	cout << m_house << endl;
	// Deal additional cards to players
	for (pPlayer = m_Players.begin(); pPlayer != m_Players.end(); ++pPlayer)
		{
			m_deck.AdditionalCards(*pPlayer);
		}
	// Reveal house's first card
	m_house.FlipFirstCard();
	cout << endl << m_house;
	// Deal additional cards to house
	m_deck.AdditionalCards(m_house);

	if (m_house.IsBusted())
		{
			// Everyone still playing wins
			for (pPlayer = m_Players.begin(); pPlayer != m_Players.end(); ++pPlayer)
			{
				if (!pPlayer->IsBusted())
				{
					pPlayer->Win();
				}
			}
		}
	else
		{
			// Compare each player still playing to the house
			for (pPlayer = m_Players.begin(); pPlayer != m_Players.end(); ++pPlayer)
			{
				if (!pPlayer->IsBusted())
				{
					pPlayer->Win();
				}
				else if (pPlayer->GetTotal() < m_house.GetTotal() || pPlayer->IsBusted())
				{
					pPlayer->Lose();
				}
				else
				{
					pPlayer->Push();
				}
			}
		}
	// Remove everyone's cards
	for (pPlayer = m_Players.begin(); pPlayer != m_Players.end(); ++pPlayer)
	{
		pPlayer->Clear();
	}
	m_house.Clear();
}

// functions that overload the insertion operator for use in the main function with the
// user-defined data types
ostream& operator<<(ostream& os, const Card& aCard);
ostream& operator<<(ostream& os, const GenericPlayer& aGenericPlayer);

int main() {
	// Greeting the player and asking how many players will be in the game
	cout << "\n\t *** Welcome to Blackjack ***\n\n";
	cout << "\nThis is a simulation of the casino card game Blackjack." << endl;
	cout << "You, and up to 6 other players will be playing against the dealer" << endl;
	cout << "The dealer will have one card face down until all other players have had their turn" << endl;
	cout << "You can choose to either hit or stay on your turn." << endl;
	cout << "The goal is to get as close to 21 without going over (busting)." << endl;

	int numPlayers = 0;
	while (numPlayers < 1 || numPlayers > 7)
	{
		cout << "How many players? (1 - 7): ";
		// Storing user input
		cin >> numPlayers;
	}

	vector<string> names;
	string name;
	for (int i = 0; i < numPlayers; ++i)
	{
		// Getting user input of the players' names and adding them to the vector 'names'
		cout << "Enter player name: ";
		cin >> name;
		names.push_back(name);
	}
	cout << endl;

	// The main game loop
	Game aGame(names);
	char again = 'y';
	while (again != 'n' && again != 'N')
	{
		aGame.Play();
		cout << "\nDo you want to play again? (Y/N): ";
		cin >> again;
	}
	return 0;
}

// Overloads the << operator so Card objects can be sent to cout
ostream& operator<<(ostream& os, const Card& aCard)
{
	const string RANKS[] = { "0", "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K" };
	const string SUITS[] = { "c", "d", "h", "s" };

	if (aCard.m_IsFaceUp)
	{
		os << RANKS[aCard.m_Rank] << SUITS[aCard.m_Suit];
	}
	else
	{
		os << "XX";
	}
	return os;
}

// Overloads the << operator to the GenericPlayer object can be sent to cout
ostream& operator<<(ostream& os, const GenericPlayer& aGenericPlayer)
{
	os << aGenericPlayer.m_Name << ":\t";
	vector<Card*>::const_iterator pCard;
	if (!aGenericPlayer.m_Cards.empty())
	{
		for (pCard = aGenericPlayer.m_Cards.begin(); pCard != aGenericPlayer.m_Cards.end(); ++pCard)
		{
			os << *(*pCard) << "\t";
		}
		if (aGenericPlayer.GetTotal() != 0)
		{
			cout << "(" << aGenericPlayer.GetTotal() << ")";
		}
	}
	else
	{
		os << "<empty>";
	}
	return os;
}