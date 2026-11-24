-- =======================================================
-- SCRIPT AUTO-FARM COMPLETO: ROUBE UM OVO (ROBLOX)
-- Arquivo: script_roube_um_ovo.lua
-- =======================================================

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")
local VirtualUser = game:GetService("VirtualUser")

local LocalPlayer = Players.LocalPlayer
local Character = LocalPlayer.Character or LocalPlayer.CharacterAdded:Wait()

-- Atualiza o personagem caso o jogador renasça
LocalPlayer.CharacterAdded:Connect(function(novoChar)
    Character = novoChar
end)

-- Configurações Globais (Valores padrão definidos dinamicamente pelo Streamlit)
_G.AutoFarmOvos = _G.AutoFarmOvos ~= nil and _G.AutoFarmOvos or true
_G.AutoMissoes = _G.AutoMissoes ~= nil and _G.AutoMissoes or true
_G.AutoChocarOvos = _G.AutoChocarOvos ~= nil and _G.AutoChocarOvos or false
_G.AutoRebirth = _G.AutoRebirth ~= nil and _G.AutoRebirth or false
_G.DistanciaColeta = _G.DistanciaColeta or 100
_G.NomeOvoParaChocar = _G.NomeOvoParaChocar or "Ovo Comum"

-- -------------------------------------------------------
-- 1. Anti-AFK (Impede desconexão automática após 20 min)
-- -------------------------------------------------------
LocalPlayer.Idled:Connect(function()
    VirtualUser:Button2Down(Vector2.new(0, 0), Workspace.CurrentCamera.CFrame)
    task.wait(1)
    VirtualUser:Button2Up(Vector2.new(0, 0), Workspace.CurrentCamera.CFrame)
    print("[ANTI-AFK] Prevencao de kick ativada com sucesso.")
end)

-- -------------------------------------------------------
-- 2. Auto Farm (Teleporta e coleta Ovos/Moedas pelo mapa)
-- -------------------------------------------------------
local function coletarOvosProximos()
    while task.wait(0.15) do
        if _G.AutoFarmOvos then
            local rootPart = Character and Character:FindFirstChild("HumanoidRootPart")
            if rootPart then
                for _, object in pairs(Workspace:GetDescendants()) do
                    if not _G.AutoFarmOvos then break end

                    -- Coleta por interacao ProximityPrompt (Tecla E)
                    if object:IsA("ProximityPrompt") then
                        local parent = object.Parent
                        if parent and (parent.Name:lower():find("ovo") or parent.Name:lower():find("egg") or parent.Name:lower():find("coin") or parent.Name:lower():find("moeda")) then
                            local dist = (rootPart.Position - parent.Position).Magnitude
                            if dist <= _G.DistanciaColeta then
                                rootPart.CFrame = parent.CFrame + Vector3.new(0, 3, 0)
                                fireproximityprompt(object)
                                task.wait(0.05)
                            end
                        end

                    -- Coleta por toque (TouchTransmitter)
                    elseif object:IsA("TouchTransmitter") and object.Parent then
                        local item = object.Parent
                        if item.Name:lower():find("ovo") or item.Name:lower():find("egg") or item.Name:lower():find("coin") or item.Name:lower():find("moeda") then
                            firetouchinterest(rootPart, item, 0)
                            firetouchinterest(rootPart, item, 1)
                        end
                    end
                end
            end
        end
    end
end

-- -------------------------------------------------------
-- 3. Auto Missões (Aceitar e Resgatar Recompensas)
-- -------------------------------------------------------
local function gerenciarMissoes()
    while task.wait(2) do
        if _G.AutoMissoes then
            -- Tenta acionar eventos de missao no ReplicatedStorage
            for _, v in pairs(ReplicatedStorage:GetDescendants()) do
                if v:IsA("RemoteEvent") and (v.Name:lower():find("quest") or v.Name:lower():find("missao") or v.Name:lower():find("claim")) then
                    pcall(function()
                        v:FireServer("All")
                        v:FireServer(1)
                        v:FireServer(true)
                    end)
                end
            end

            -- Interage com NPCs de missoes espalhados no mapa
            local missoesFolder = Workspace:FindFirstChild("Quests") or Workspace:FindFirstChild("Missoes") or Workspace:FindFirstChild("NPCs")
            if missoesFolder then
                for _, npc in pairs(missoesFolder:GetChildren()) do
                    local prompt = npc:FindFirstChildWhichIsA("ProximityPrompt", true)
                    if prompt then
                        fireproximityprompt(prompt)
                    end
                end
            end
        end
    end
end

-- -------------------------------------------------------
-- 4. Auto Chocar Ovos (Hatch Automatico)
-- -------------------------------------------------------
local function chocarOvosAutomatico()
    while task.wait(0.5) do
        if _G.AutoChocarOvos then
            for _, v in pairs(ReplicatedStorage:GetDescendants()) do
                if v.Name:lower():find("hatch") or v.Name:lower():find("open") or v.Name:lower():find("egg") then
                    pcall(function()
                        if v:IsA("RemoteFunction") then
                            v:InvokeServer(_G.NomeOvoParaChocar, 1)
                        elseif v:IsA("RemoteEvent") then
                            v:FireServer(_G.NomeOvoParaChocar, 1)
                        end
                    end)
                end
            end
        end
    end
end

-- -------------------------------------------------------
-- 5. Auto Rebirth (Renascer para ganhar multiplicadores)
-- -------------------------------------------------------
local function autoRebirth()
    while task.wait(3) do
        if _G.AutoRebirth then
            for _, v in pairs(ReplicatedStorage:GetDescendants()) do
                if v.Name:lower():find("rebirth") or v.Name:lower():find("renascer") then
                    pcall(function()
                        if v:IsA("RemoteEvent") then
                            v:FireServer()
                        elseif v:IsA("RemoteFunction") then
                            v:InvokeServer()
                        end
                    end)
                end
            end
        end
    end
end

-- -------------------------------------------------------
-- Execução Paralela das Funções
-- -------------------------------------------------------
task.spawn(coletarOvosProximos)
task.spawn(gerenciarMissoes)
task.spawn(chocarOvosAutomatico)
task.spawn(autoRebirth)

print("--------------------------------------------------")
print("[ROUBE UM OVO] Script principal carregado com sucesso!")
print("--------------------------------------------------")
