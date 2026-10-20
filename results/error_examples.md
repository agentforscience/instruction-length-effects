# Paired flips: standard correct -> exhaustive wrong

### qwen2.5-0.5b / cls / ag3391: standard correct, exhaustive wrong
- gold: `Sports`
- standard: `'Sports'`
- exhaustive: `'Business'`

### qwen2.5-0.5b / cls / ag331: standard correct, exhaustive wrong
- gold: `Sports`
- standard: `'Sports'`
- exhaustive: `'Business'`

### qwen2.5-0.5b / ext / 5705eb3375f01819005e7764: standard correct, exhaustive wrong
- gold: `['Hollywood']`
- standard: `'Hollywood'`
- exhaustive: `'The Walt Disney Company'`

### qwen2.5-0.5b / ext / 56e122dacd28a01900c67639: standard correct, exhaustive wrong
- gold: `['eugenics', 'imposed selective breeding version of eugenics']`
- standard: `'Eugenics'`
- exhaustive: `'Tesla a fan of eugenics.'`

### qwen2.5-0.5b / rsn / gsm478: standard correct, exhaustive wrong
- gold: `621`
- standard: `'going on the tour:**\n   - Total number of people = Total number of employees + Total number of tour guides.\n   - Total number of people = 600 employees + 21 tour guides = 621 people.\n\nFinal answer: The total number of people going on the tour is 621.'`
- exhaustive: `'ng on the tour:**\n   - Total number of people = Total number of employees + Total number of tour guides\n   - Total number of people = 1800 employees + 21 tour guides = 1821 people.\n\nTherefore, the total number of people going on the tour is **1821**.'`

### qwen2.5-0.5b / rsn / gsm704: standard correct, exhaustive wrong
- gold: `50`
- standard: `' 60\\) dollars.\n   - Julia received \\(2 \\times 20 = 40\\) dollars.\n\n4. Gerald spent $10 on a book. So, the amount of money he has left is:\n   \\[\n   \\text{Money left} = 60 - 10 = 50 \\text{ dollars}\n   \\]\n\nTherefore, the final answer is:\n\\[\n\\boxed{50}\n\\]'`
- exhaustive: `'s:\n\\[ \\frac{100}{5} = 20 \\]\n\nNow, we need to find out how much money Gerald has left after spending $10. Gerald originally had $20, so after spending $10, he has:\n\\[ 20 - 10 = 10 \\]\n\nTherefore, the amount of money Gerald has left is:\n\\[ \\boxed{10} \\]'`

### qwen2.5-1.5b / cls / ag1347: standard correct, exhaustive wrong
- gold: `Business`
- standard: `'Business'`
- exhaustive: `'World'`

### qwen2.5-1.5b / cls / ag2412: standard correct, exhaustive wrong
- gold: `Sci/Tech`
- standard: `'Sci/Tech'`
- exhaustive: `'World'`

### qwen2.5-1.5b / ext / 5725cb4a89a1e219009abec8: standard correct, exhaustive wrong
- gold: `['three', 'three astronauts']`
- standard: `'three'`
- exhaustive: `'3'`

### qwen2.5-1.5b / ext / 5727ee372ca10214002d99ec: standard correct, exhaustive wrong
- gold: `['entrepreneurship rates']`
- standard: `'entrepreneurship rates'`
- exhaustive: `'higher economic inequality tends to increase entrepreneurship rates at the individual level (self-employment).'`

### qwen2.5-1.5b / rsn / gsm44: standard correct, exhaustive wrong
- gold: `20`
- standard: `'ng 20 candles:**\n   - Each candle is sold for $2.00.\n   - Revenue from 20 candles = 20 candles * $2.00/candle = $40.00\n\n3. **Calculate the net profit:**\n   - Net profit = Revenue - Cost\n   - Net profit = $40.00 - $20.00 = $20.00\n\nFinal answer: $20.00'`
- exhaustive: `"les * $2.00 per candle = $40.00.\n\n3. **Calculate the net profit:**\n   - Net profit = Revenue - Cost of supplies\n   - Net profit = $40.00 - $10.00 = $30.00.\n\nTherefore, Charlie's net profit if he makes and sells 20 candles is $30.00.\n\nFinal answer: 30"`

### qwen2.5-1.5b / rsn / gsm239: standard correct, exhaustive wrong
- gold: `280`
- standard: `'st of the students went out through exit C.\n   - Number of students who went out through exit C = Remaining students after exit B\n   - Number of students who went out through exit C = 280 students.\n\nFinal answer: 280 students went out through exit C.'`
- exhaustive: `' who went out through exit C:**\n   - The rest of the students went out through exit C.\n   - Number of students who went out through exit C = Remaining students\n   - Number of students who went out through exit C = 580 students.\n\n**Final answer: 580**'`

### qwen2.5-14b / cls / ag4069: standard correct, exhaustive wrong
- gold: `Sci/Tech`
- standard: `'Sci/Tech'`
- exhaustive: `'Business'`

### qwen2.5-14b / cls / ag4571: standard correct, exhaustive wrong
- gold: `Business`
- standard: `'Business'`
- exhaustive: `'Sci/Tech'`

### qwen2.5-14b / rsn / gsm901: standard correct, exhaustive wrong
- gold: `1`
- standard: `' 2 child bowls.\n\n7. Determine how many times each child can have a bowl of soup from the leftover soup:\n   - There are 2 child bowls left.\n   - There are 2 children.\n   - Each child can have 2 / 2 = 1 bowl of soup from the leftovers.\n\nFinal answer: 1'`
- exhaustive: `'r lunch from the leftover soup.\n\nStep 8: Verify the final answer:\n- The question asks how many times each child will be able to have a bowl of soup for lunch from the leftover soup, and the answer is 2, which matches the calculation.\n\nFinal answer: 2'`

### qwen2.5-14b / rsn / gsm781: standard correct, exhaustive wrong
- gold: `17`
- standard: `' other two pizzas} = \\frac{34}{2} = 17 \\text{ dollars}\n   \\]\n\n4. **Check the final answer:**\n   - The cost of each of the other two pizzas is 17 dollars, which is reasonable given the total cost and the cost of the first two pizzas.\n\nFinal answer: 17'`
- exhaustive: `'f the other two pizzas is 2 dollars, which is reasonable.\n\nStep 7: The final answer is 2 dollars per pizza.\n\nStep 8: The question asks for the cost of each of the other two pizzas, and the final number answers exactly what was asked.\n\nFinal answer: 2'`

### qwen2.5-3b / cls / ag3117: standard correct, exhaustive wrong
- gold: `Sports`
- standard: `'Sports'`
- exhaustive: `'Business'`

### qwen2.5-3b / cls / ag3140: standard correct, exhaustive wrong
- gold: `Sci/Tech`
- standard: `'Sci/Tech'`
- exhaustive: `'Business'`

### qwen2.5-3b / ext / 5729723c6aef051400154ee8: standard correct, exhaustive wrong
- gold: `['light reactions', 'each stage of photosynthesis']`
- standard: `'light reactions'`
- exhaustive: `'store CO2 in a four-carbon compound'`

### qwen2.5-3b / ext / 572928bf6aef051400154af0: standard correct, exhaustive wrong
- gold: `['six gold', 'several', 'six']`
- standard: `'six'`
- exhaustive: `'6'`

### qwen2.5-3b / rsn / gsm710: standard correct, exhaustive wrong
- gold: `45`
- standard: `' $10.00 + $12.00 + $13.00 = $50.00\n\nStep 3: Calculate the discount amount.\nDiscount = 10% of $50.00 = 0.10 * $50.00 = $5.00\n\nStep 4: Calculate the total cost after the discount.\nTotal cost after discount = $50.00 - $5.00 = $45.00\n\nFinal answer: 45.00'`
- exhaustive: `'00 + $12.00 + $13.00 = $49.00\n\nStep 3: Calculate the discount amount.\nDiscount = 10% of $49.00 = 0.10 * $49.00 = $4.90\n\nStep 4: Subtract the discount from the total cost to get the final bill.\nFinal bill = $49.00 - $4.90 = $44.10\n\nFinal answer: 44.10'`

### qwen2.5-3b / rsn / gsm1237: standard correct, exhaustive wrong
- gold: `78`
- standard: `'our calculation shows that there were 78 teachers present.\n   - This answer is reasonable because it is less than the total number of teachers (82) and includes both the teachers who were not sick and the substitute teachers.\n\n5. **Final answer: 78**'`
- exhaustive: `'9\n- 69 - 9 = 60\n\nStep 6: Verify the intermediate result.\n- 69 is a plausible number of teachers.\n- 60 is a plausible number of teachers.\n\nStep 7: Combine the intermediate results to obtain the final answer.\n- Teachers at school = 60\n\nFinal answer: 60'`

### qwen2.5-7b / cls / ag4069: standard correct, exhaustive wrong
- gold: `Sci/Tech`
- standard: `'Sci/Tech'`
- exhaustive: `'Business'`

### qwen2.5-7b / cls / ag4625: standard correct, exhaustive wrong
- gold: `Sports`
- standard: `'Sports'`
- exhaustive: `'World'`

### qwen2.5-7b / ext / 571136b8a58dae1900cd6d22: standard correct, exhaustive wrong
- gold: `['Corliss', 'patent valve']`
- standard: `'Corliss'`
- exhaustive: `'Corliss, and later, poppet valve gears'`

### qwen2.5-7b / rsn / gsm240: standard correct, exhaustive wrong
- gold: `21`
- standard: `"ames has 6 more candies than Robert, so: \\(\\text{James's candies} = 27 + 6 = 33\\).\n\nStep 4: Calculate how many more candies John has than James.\n- John has 54 candies, and James has 33 candies.\n- The difference is: \\(54 - 33 = 21\\).\n\nFinal answer: 21"`
- exhaustive: `'le given John has 54.\n- James has 21 candies, which is 6 less than Robert, also reasonable.\n- The difference of 33 candies is a plausible number given the context.\n\nStep 7: Combine the intermediate results to obtain the final answer.\nFinal answer: 33'`

### qwen2.5-7b / rsn / gsm453: standard correct, exhaustive wrong
- gold: `6400`
- standard: `"orth $1200, so 2 rubies are worth 2 * $1200 = $2400.\n\nStep 6: Calculate the total value of all Jenna's jewels.\n- The total value is the sum of the value of the sapphires and the value of the rubies, which is $4000 + $2400 = $6400.\n\nFinal answer: 6400"`
- exhaustive: `'to obtain the final answer.\nTotal value: \\(\\$2400 + \\$2400 + \\$4000 = \\$8800\\)\n\nStep 7: Verify the result.\n- The total value is a plausible sum given the values of the sapphires and rubies.\n- The units are in dollars, as required.\n\nFinal answer: 8800'`

### sys_qwen2.5-0.5b / cls / ag4186: standard correct, exhaustive wrong
- gold: `Sci/Tech`
- standard: `'Sci/Tech'`
- exhaustive: `'World'`

### sys_qwen2.5-0.5b / cls / ag5477: standard correct, exhaustive wrong
- gold: `Sci/Tech`
- standard: `'Sci/Tech'`
- exhaustive: `'Business'`

### sys_qwen2.5-0.5b / ext / 5725db98ec44d21400f3d6c5: standard correct, exhaustive wrong
- gold: `["Fresno's far southeast side", 'far southeast side']`
- standard: `"Fresno's far southeast side"`
- exhaustive: `"Sunnyside is located on Fresno's far southeast side, bounded by Chestnut Avenue to the West."`

### sys_qwen2.5-0.5b / ext / 572973f76aef051400154f0a: standard correct, exhaustive wrong
- gold: `['2']`
- standard: `'2'`
- exhaustive: `'6'`

### sys_qwen2.5-0.5b / rsn / gsm44: standard correct, exhaustive wrong
- gold: `20`
- standard: `'is the total revenue minus the total cost.\n   - Net profit for 20 candles:\n     \\[\n     40.00 \\text{ dollars} - 20.00 \\text{ dollars} = 20.00 \\text{ dollars}\n     \\]\n\n5. **Write the final answer:**\n   - The net profit is $20.00.\n\nFinal answer: $20.00'`
- exhaustive: `"tal revenue minus total cost.\n   - Profit = $40.00 - $20.00 = $20.00.\n\n5. **Determine the net profit:**\n   - The net profit is the profit minus the cost of beeswax.\n   - Net profit = $20.00 - $20.00 = $0.00.\n\nTherefore, Charlie's net profit is $0.00."`

### sys_qwen2.5-0.5b / rsn / gsm506: standard correct, exhaustive wrong
- gold: `144`
- standard: `'of snowshoes:**\n   Each pair of snowshoes costs $12.00, so for 12 pairs:\n   \\[\n   12 \\text{ pairs} \\times \\$12.00/pair = \\$144.00\n   \\]\n\n5. **Final answer:**\n   The total cost for Mario to buy snowshoes for all his dogs is:\n   \\[\n   \\boxed{144}\n   \\]'`
- exhaustive: `'pair of snowshoes costs $12.00. Therefore, the total cost for 48 pairs is:\n   \\[\n   48 \\text{ pairs} \\times 12 \\text{ dollars/pair} = 576 \\text{ dollars}\n   \\]\n\nThus, the total cost for Mario to buy snowshoes for all of his dogs is:\n\\[\n\\boxed{576}\n\\]'`

### sys_qwen2.5-1.5b / cls / ag6069: standard correct, exhaustive wrong
- gold: `Business`
- standard: `'Business'`
- exhaustive: `'Sports'`

### sys_qwen2.5-1.5b / cls / ag4186: standard correct, exhaustive wrong
- gold: `Sci/Tech`
- standard: `'Sci/Tech'`
- exhaustive: `'World'`

### sys_qwen2.5-1.5b / ext / 5725cb4a89a1e219009abec8: standard correct, exhaustive wrong
- gold: `['three', 'three astronauts']`
- standard: `'three'`
- exhaustive: `'3'`

### sys_qwen2.5-1.5b / ext / 56e748a200c9c71400d76f37: standard correct, exhaustive wrong
- gold: `['cultures']`
- standard: `'cultures'`
- exhaustive: `'cultural factors'`

### sys_qwen2.5-1.5b / rsn / gsm1113: standard correct, exhaustive wrong
- gold: `-3`
- standard: `' Initial temperature - 8\n   New temperature = 2 - 8 = -6 degrees Celsius\nStep 3: Temperature increased by 3 degrees Celsius in the morning\n   Final temperature = New temperature + 3\n   Final temperature = -6 + 3 = -3 degrees Celsius\n\nFinal answer: -3'`
- exhaustive: `'se.\nStep 5: 2 - 8 + 3 = -3\nStep 6: After adding the decrease, we have -3 degrees Celsius.\nStep 7: Adding the increase of 3 degrees Celsius to the result gives us -3 + 3 = 0\nStep 8: The temperature in the morning is 0 degrees Celsius.\n\nFinal answer: 0'`

### sys_qwen2.5-1.5b / rsn / gsm1211: standard correct, exhaustive wrong
- gold: `448`
- standard: `'p 1: Calculate the amount of the second medicine.\n14 mL * 3 = 42 mL\n\nStep 2: Calculate the total amount of medicine for one dose.\n14 mL + 42 mL = 56 mL\n\nStep 3: Calculate the total amount of medicine for 8 doses.\n56 mL * 8 = 448 mL\n\nFinal answer: 448'`
- exhaustive: `'t of the second medicine.\n14 mL + 3 * 14 mL = 14 mL + 42 mL = 56 mL\n\nStep 2: Calculate the total amount of medicine for one dose.\n14 mL + 56 mL = 70 mL\n\nStep 3: Calculate the total amount of medicine for 8 doses.\n70 mL * 8 = 560 mL\n\nFinal answer: 560'`
