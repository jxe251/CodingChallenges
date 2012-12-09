require 'set'

if ARGV.length < 2
    puts "Invalid Arguments"
    exit(-1)
end

# don't try with more than 20 elements
def Powerset(set)
    #start = Time.now
    ret = set.class[set.class[]]
    set.each do |s|
        deepcopy = ret.map { |x| set.class.new(x) }
        deepcopy.map { |r| r << s }
        ret = ret + deepcopy
    end
    return ret#, Time.now - start
end

# takes in hash of food combos in form of:
#    {["food1"] => 1.0, ["food1", "food2"] -> 3.0}
# returns powerset of keys in a hash paired total price of keys per set
# does not remove duplicates in sets
def WeightedPowerset(comboVals)
    #start = Time.now
    ret = [[[] , 0.0]]
    foodCombos = comboVals.keys
    foodCombos.each do |combo|
        cpyArryFlt = ->(y) { y.kind_of?(Array) ? y.map { |z| z } : y }
        deepcopy = ret.map { |comboVal| comboVal.map { |y| cpyArryFlt[y] } }
        deepcopy = deepcopy.map { |d| [d[0] + combo, d[1] + comboVals[combo]] }
        ret = ret + deepcopy
    end
    return Hash[ret]#, Time.now - start
end

menuPath, *wantList  = ARGV
wantCount = Hash[wantList.zip]
wantSet = Set.new(wantList)
wantList = Hash[wantList.zip]
wantCount.each_key do |key|
    wantCount[key] = wantList.count(key)
    wantList[key] = false
end

begin
    file = File.new(menuPath, "r")
rescue => err
    puts "Exception: #{err}"
end

restaurants = {}
menuItems = Array.new
MenuItem = Struct.new :RestNo, :Price, :Foods
while (line = file.gets)
    restNo, price, *foods = line.split(/, /)
    foods.last.strip!
    #foods = Set.new(foods)
    # ignore listing if nothing wanted
    next if (wantSet & foods).empty?

    restNo = Integer(restNo)
    price = Float(price)
    restaurants[restNo] = [] if !restaurants.key?(restNo)
    item = MenuItem.new(restNo, price, foods)
    restaurants[restNo].push(item)
    menuItems.push(item)
end

if $DEBUG
    puts "Relevant menu by restaurant:"
    puts "#{restaurants}"
end

def AnalyzeCheapest(menuItems, wantSet)
    #menuItems.sort!{|a, b| a.RestNo <=> b.RestNo }
    foodSetPrices = Hash[menuItems.map { |x| [x.Foods, x.Price] }]
    poweredSets = WeightedPowerset(foodSetPrices)

    if $DEBUG
        puts "Relevant menu:"
        puts "#{menuItems}"
        puts "Relevant foodSets:"
        puts "#{foodSetPrices}"
        puts "Powered Sets:"
        puts "#{poweredSets}"
        poweredSets.each { |set, price| puts "#{Set.new(set).inspect}" }
    end

    poweredSets.delete_if { |set, price| !Set.new(set).superset?(wantSet) }
    sortedSets = poweredSets.sort{ |a, b| a[1] <=> b[1] }

    if $DEBUG
        puts "Filtered out unsatisfying sets:"
        puts "#{poweredSets}"
        puts "Sort filtered:"
        puts "#{sortedSets}"
        puts "Return local solution:"
        puts "#{sortedSets.each.peek[1]}"
    end
    return sortedSets.each.peek[1]
end

results = restaurants.map { |rest, foodCombos| [rest, AnalyzeCheapest(foodCombos, wantSet)] }
puts "Results"
result = (results.sort! { |a, b| a[1] <=> b[1] }).first
puts "#{result[0]}, #{result[1]}"
