require 'set'

# takes in any collection of items and returns their powerset
# don't try with more than 20 elements
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

# takes in hash of sets and their cost in form of:
#    {["item1"] => 1.0, ["item1", "item2"] => 3.0}
# returns powerset of keys in a hash paired total price of keys per set
# does not remove duplicates in sets
def WeightedPowerset(setCosts)
    puts "setCosts:\n #{setCosts}" if $DEBUG
    #start = Time.now
    ret = [[[] , 0.0]]
    foodCombos = setCosts.keys
    cpyArryFlt = ->(y) { y.kind_of?(Array) ? y.map { |z| z } : y }
    foodCombos.each do |combo|
        deepcopy = ret.map { |comboVal| comboVal.map { |y| cpyArryFlt[y] } }
        deepcopy = deepcopy.map { |d| [d[0] + combo, d[1] + setCosts[combo]] }
        ret += deepcopy
    end
    puts "return:\n #{Hash[ret]}" if $DEBUG
    return Hash[ret]#, Time.now - start
end

# setCosts is a hashed collection of sets and their costs
# universe is the set to cover
# returns sets that cover the universe, minimizing cost, and total cost
def PowersetSetCover(setCosts, universe)
    #powerSets = WeightedPowerset(setCosts)
    powerSets = Powerset(setCosts.keys)
    puts "PowerSets:\n #{powerSets}" if $DEBUG

    def SumEachBy(collection, getValueFunc)
        sum = 0
        collection.each { |x| sum += getValueFunc[x] }
        return sum
    end
    getSetCost = ->(x) { setCosts[x] }
    powerSets = powerSets.map { |set| [set, SumEachBy(set, getSetCost)] }
    puts "powerSetCosts:\n}" if $DEBUG

    powerSets.reject! { |set| !Set.new(set.flatten).superset?(universe) }
    puts "powerSetsFiltered:\n #{powerSets}" if $DEBUG
    
    return nil if powerSets.size == 0

    powerSets.sort! { |a, b| a[1] <=> b[1] }
    puts "Sort filtered:\n #{powerSets}" if $DEBUG
    puts "Return local solution:\n #{powerSets.first}" if $DEBUG
    return powerSets.first
end

# setCosts is a hashed collection of sets and their costs
# universe is the set to cover
# returns sets that cover the universe, minimizing cost, and total cost
def GreedyWeightedSetCover(setCosts, universe)
    puts "setCosts:\n #{setCosts}" if $DEBUG
    puts "universe:\n #{universe.inspect}" if $DEBUG
    minCover = setCosts.select { |set, cost| cost == 0 }
    cover = Set.new(minCover.keys.flatten!)
    puts "cover:\n #{cover.inspect}" if $DEBUG
    setCosts.reject! { |set, cost| cost == 0 }
    setValue = setCosts.map { |set, cost| [set, (Set.new(set) & universe).size / cost] }
    setValue.sort! { |a, b| a[1] <=> b[1] }
    puts "setValue:\n #{setValue.inspect}" if $DEBUG
    while !cover.superset?(universe)
        puts "minCover:\n #{minCover.inspect}, #{setValue.size}" if $DEBUG
        puts "cover:\n #{cover.inspect}" if $DEBUG
        return nil if setValue.size == 0
        setVal = setValue.pop
        puts "setVal:\n #{setVal}" if $DEBUG
        minCover[setVal[0]] = setCosts[setVal[0]]
        cover += setVal[0]
    end
    ret = [[], 0]
    minCover.each { |set, cost| ret[0] << set; ret[1] += cost }
    puts "finalret:\n #{ret}" if $DEBUG
    return ret
end

# takes a collection of menuItem (a set of sets) and a unique set of wanted foods
def AnalyzeCheapest(menuItems, wantSet)
    #menuItems.sort! {|a, b| a.RestNo <=> b.RestNo }
    foodSetPrices = Hash[menuItems.map { |x| [x.Foods, x.Price] }]
    puts "Relevant foodSets:\n #{foodSetPrices}" if $DEBUG

    #potentially expensive
    puts "problem size: #{foodSetPrices.size}\n #{foodSetPrices}" if $DEBUG
    problemTooBig = foodSetPrices.size > 15
    puts "#{problemTooBig ? "Greedy Approximation" : "Exhaustive Search"}" if $DEBUG

    if problemTooBig
        return GreedyWeightedSetCover(foodSetPrices, wantSet) if problemTooBig
    else
        return PowersetSetCover(foodSetPrices, wantSet)
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

puts "wantSet:\n" "#{wantSet.inspect}" if $DEBUG

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
    puts "Do I want: #{foods}\n #{!(wantSet & foods).empty?}" if $DEBUG
    next if (wantSet & foods).empty?

    #consider repeats as unique foods by copying
    foods = ToUniqueSet(foods)

    #add foods to restaurant menu
    restNo = Integer(restNo)
    price = Float(price)
    restaurants[restNo] = [] if !restaurants.key?(restNo)
    restFoodSets[restNo] = Set[] if !restFoodSets.key?(restNo)
    # add copy as long as additional copy can still satisfy
    copy = 0
    appendedFoods = Set[]
    loop do
        unsatisfied = wantSet - appendedFoods
        puts "considering : #{appendedFoods}\n  #{unsatisfied.inspect}" if $DEBUG
        appendedFoods = foods.map { |f| "#{f}#{"_" * copy}" }
        foodsCanSatisfy = (unsatisfied - appendedFoods).size < unsatisfied.size
        break if !foodsCanSatisfy
        restaurants[restNo].push(MenuItem.new(restNo, price, appendedFoods))
        #restFoodSets[restNo] += appendedFoods
        copy += 1
    end
end

puts "Relevant menu by restaurant:\n #{restaurants}" if $DEBUG

#not sure if this is neccessary after addition of foodsCanSatisfy check
#restaurants.reject!{ |rest, foodCombos| !restFoodSets[rest].superset?(wantSet) }
if restaurants.empty?
    puts nil
    exit(0)
end

results = restaurants.map { |rest, foodCombos| [rest, AnalyzeCheapest(foodCombos, wantSet)] }
puts "results:\n #{results}" if $DEBUG

if results.empty?
    puts nil
    exit(0)
end

results.sort! { |a, b| a[1][1] <=> b[1][1] }
puts "sortedResults:\n #{results}"#if $DEBUG
answer = results.first
puts "#{answer[0]}, #{answer[1][1]}"

