require 'set'

# takes in any collection of items and returns their powerset
# don't try with more than 20 elements
# TODO optimize bottleneck
def Powerset(set)
    #start = Time.now
    ret = set.class[set.class[]]
    set.each do |s|
        deepcopy = ret.map { |x| set.class.new(x) }
        deepcopy.map { |r| r << s }
        ret += deepcopy
    end
    return ret#, Time.now - start
end

# setCosts is a hashed collection of sets and their costs
# universe is the set to cover
# returns sets that cover the universe, minimizing cost, and total cost
# searches exhaustively through all powerset combinations
def PowersetSetWeightedCover(setCosts, universe)
    powerSets = Powerset(setCosts.keys)
    sumSets = ->(sets) { sets.reduce(0) {|sum, x| sum + setCosts[x] } }
    powerSets = powerSets.map { |set| [set, sumSets[set]] }
    powerSets.select! { |set| Set.new(set.flatten).superset?(universe) }
    return nil if powerSets.size == 0
    powerSets.sort! { |a, b| a[1] <=> b[1] }
    return powerSets.first
end

# setCosts is a hashed collection of sets and their costs
# universe is the set to cover
# returns sets that cover the universe, minimizing cost, and total cost
# searches greedily to find an approximate solution
# http://greedyalgs.info/blog/greedy-set-cover/ (other methods here)
# http://mathoverflow.net/questions/41362/analyzing-weighted-set-cover-variant
# TODO: try linear programming relaxation
def GreedyWeightedSetCover(setCosts, universe)
    minCover = setCosts.select { |set, cost| cost == 0 }
    setCosts.reject! { |set, cost| cost == 0 }
    setValue = setCosts.map {
        |set, cost| [set, (Set.new(set) & universe).size / cost]
    }
    setValue.sort! { |a, b| a[1] <=> b[1] }
    cover = Set.new(minCover.keys.flatten!)
    while !cover.superset?(universe)
        return nil if setValue.size == 0
        setVal = setValue.pop
        minCover[setVal[0]] = setCosts[setVal[0]]
        cover += setVal[0]
    end
    ret = [[], 0]
    minCover.each { |set, cost| ret[0] << set; ret[1] += cost }
    return ret
end

# takes a collection of MenuItem and a unique set of wanted foods
# returns cheapest combination that satisfies wantSet and its price
def GetCheapestSet(menuItems, wantSet)
    foodSetPrices = Hash[menuItems.map { |x| [x.Foods, x.Price] }]

    #potentially expensive, try to minimize size
    problemTooBig = foodSetPrices.size > 15

    if problemTooBig
        return GreedyWeightedSetCover(foodSetPrices, wantSet)
    else
        return PowersetSetWeightedCover(foodSetPrices, wantSet)
    end
end

def ToUniqueSet(foodList)
    ret = Set[]
    foodList.each do |food|
        while ret.include?(food)
            food = "#{food}_"
        end
        ret << food
    end
    return ret
end

if ARGV.length < 2
    puts "Invalid Arguments"
    exit(-1)
end

menuPath, *wantList  = ARGV
wantSet = ToUniqueSet(wantList)

begin
    file = File.new(menuPath, "r")
rescue => err
    puts "Exception: #{err}"
end

restaurants = {}
restFoodSets = {}
MenuItem = Struct.new :RestNo, :Price, :Foods
# assuming every line is well formatted
while (line = file.gets)
    restNo, price, *foods = line.split(/, /)
    foods.last.strip!
    # ignore listing if nothing wanted
    next if (wantSet & foods).empty?

    # consider repeats within a combo as unique foods by copying
    foods = ToUniqueSet(foods)
    restNo = Integer(restNo)
    price = Float(price)
    restaurants[restNo] = [] if !restaurants.key?(restNo)
    restFoodSets[restNo] = Set[] if !restFoodSets.key?(restNo)
    def append_(food, occurred)
        while occurred.include?(food)
            food = "#{food}_"
        end
        occurred << food
        return food
    end
    
    # add foods to restaurant menu
    # for each combo, add copy as long as additional copy satisfies even more
    # within the scope of each set of combo copies,
    # append '_' to each food items per occurrence
    copy = 0
    appendedFoods = Set[]
    occurred = Set[]
    loop do
        unsatisfied = wantSet - appendedFoods
        appendedFoods = foods.map { |f| append_(f, occurred) }
        canSatisfyMore = (unsatisfied - appendedFoods).size < unsatisfied.size
        break if !canSatisfyMore
        restaurants[restNo].push(MenuItem.new(restNo, price, appendedFoods))
        #restFoodSets[restNo] += appendedFoods
        copy += 1
    end
end

#not sure if this is neccessary after addition of foodsCanSatisfy check
#restaurants.select! { |rest, foodCombos| restFoodSets[rest].superset?(wantSet) }
if restaurants.empty?
    puts nil
    exit(0)
end

results = restaurants.map {
    |num, menuItems| [num, GetCheapestSet(menuItems, wantSet)]
}
results.reject! { |x| x[1] == nil }
results.sort! { |a, b| a[1][1] <=> b[1][1] }
if results.empty?
    puts nil
    exit(0)
end
answer = results.first
puts "#{answer[0]}, #{answer[1][1]}"
