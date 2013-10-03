

-- Edit box
	local ebox = CreateFrame('EditBox','Filibox')
		ebox:SetAutoFocus(false)
		ebox:ClearFocus()


-- Timer
	local FREQ = 1/20
	
	local timers = {
	--	{cmd, delay},
	--	{'/say hi', 3},  --  /say hi in 3 sec
	}
	
	local throttle = 0
	local function OnUpdate(self,elapsed)
		throttle = throttle + elapsed
		if throttle >= FREQ then
			local t,cmd,delay
			for i = #timers,1,-1 do
				t = timers[i]
				cmd,delay = t[1],t[2]
				delay = delay - throttle
				if delay <= 0 then
					self:SetText(cmd)
					ChatEdit_SendText(self)
					self:Show()
					tremove(timers,i)
				else
					t[2] = delay
				end
			end
			throttle = 0
		end
		if #timers == 0 then
			self:Hide()
		end
	end
	ebox:SetScript('OnUpdate',OnUpdate)
	ebox:Hide()


-- Slash cmd
	SLASH_FILIBUSTER1 = '/in'
	SLASH_FILIBUSTER2 = '/delay'
	SLASH_FILIBUSTER3 = '/wait'
	
	SlashCmdList['FILIBUSTER'] = function(input)
		local delay,cmd,args = input:match('^%s*(%d+%.?%d*)%s+(/%S+)(.*)$')
		
		delay = tonumber(delay)
		if not delay then
			print('|cff7fffffFilibuster|r: Incorrect usage. Example: |cffffff7f/in 6 /say Hello, world!|r.')
			return
		end
		
		if IsSecureCmd(cmd) then
			print('|cff7fffffFilibuster|r: |cffff7f7fError|r: Unable to execute secure command |cffffff7f'..cmd..'|r.')
			return
		end
		
		timers[#timers+1] = {(cmd..args),delay}
		ebox:Show()
	end
