import pygame


animaciones_personaje_1 = {
    'correr': [
        pygame.image.load("Huntress/Run_0.png"),
        pygame.image.load("Huntress/Run_1.png"),
        pygame.image.load("Huntress/Run_2.png"),
        pygame.image.load("Huntress/Run_3.png"),
        pygame.image.load("Huntress/Run_4.png"),
        pygame.image.load("Huntress/Run_5.png"),
        pygame.image.load("Huntress/Run_6.png"),
        pygame.image.load("Huntress/Run_7.png")
    ],  
    'saltar': [
        pygame.image.load("Huntress/Jump_0.png"),
        pygame.image.load("Huntress/Jump_1.png"),
    ],  
    'atacar': [
        pygame.image.load("Huntress/Attack_0.png"),
        pygame.image.load("Huntress/Attack_1.png"),
        pygame.image.load("Huntress/Attack_2.png"),
        pygame.image.load("Huntress/Attack_3.png"),
        pygame.image.load("Huntress/Attack_4.png"),
        pygame.image.load("Huntress/Attack_5.png"),
        
    ],  
    
    'quieto': [
        pygame.image.load("Huntress/Idle_0.png"),
        pygame.image.load("Huntress/Idle_1.png"),
        pygame.image.load("Huntress/Idle_2.png"),
        pygame.image.load("Huntress/Idle_3.png"),
        pygame.image.load("Huntress/Idle_4.png"),
        pygame.image.load("Huntress/Idle_5.png"),
        pygame.image.load("Huntress/Idle_6.png"),
        pygame.image.load("Huntress/Idle_7.png"),
        pygame.image.load("Huntress/Idle_8.png"),
        pygame.image.load("Huntress/Idle_9.png")
    ],  
    'flecha': [
        pygame.image.load("Huntress/Arrow_Static.png")
    ],
    
}

animaciones_personaje_2 = {
    'correr': [
        pygame.image.load("Soulhunter/Run_0.png"),
        pygame.image.load("Soulhunter/Run_1.png"),
        pygame.image.load("Soulhunter/Run_2.png"),
        pygame.image.load("Soulhunter/Run_3.png"),
        pygame.image.load("Soulhunter/Run_4.png"),
        pygame.image.load("Soulhunter/Run_5.png"),
        pygame.image.load("Soulhunter/Run_6.png")
    ],  
    'saltar': [
        pygame.image.load("Soulhunter/Jump_0.png")
    ],  
    'atacar': [
        pygame.image.load("Soulhunter/Attack_0.png"),
        pygame.image.load("Soulhunter/Attack_1.png"),
        pygame.image.load("Soulhunter/Attack_2.png"),
        pygame.image.load("Soulhunter/Attack_3.png"),
        pygame.image.load("Soulhunter/Attack_4.png")
    ],  
    'quieto': [
        pygame.image.load("Soulhunter/Idle_0.png"),
        pygame.image.load("Soulhunter/Idle_1.png"),
        pygame.image.load("Soulhunter/Idle_2.png"),
        pygame.image.load("Soulhunter/Idle_3.png"),
        pygame.image.load("Soulhunter/Idle_4.png")
    ],  
    
}


animaciones_boss= { 
    'habilidad': [
        pygame.image.load("Undead executioner/Skill_0.png"),
        pygame.image.load("Undead executioner/Skill_1.png"),
        pygame.image.load("Undead executioner/Skill_2.png"),
        pygame.image.load("Undead executioner/Skill_3.png"),
        pygame.image.load("Undead executioner/Skill_4.png"),
        pygame.image.load("Undead executioner/Skill_5.png"),
        pygame.image.load("Undead executioner/Skill_6.png"),
        pygame.image.load("Undead executioner/Skill_7.png"),
        pygame.image.load("Undead executioner/Skill_8.png"),
        pygame.image.load("Undead executioner/Skill_9.png"),
        pygame.image.load("Undead executioner/Skill_10.png"),
        pygame.image.load("Undead executioner/Skill_11.png")
    ],  
    'atacar': [
        pygame.image.load("Undead executioner/Attack_0.png"),
        pygame.image.load("Undead executioner/Attack_1.png"),
        pygame.image.load("Undead executioner/Attack_2.png"),
        pygame.image.load("Undead executioner/Attack_3.png"),
        pygame.image.load("Undead executioner/Attack_4.png"),
        pygame.image.load("Undead executioner/Attack_5.png"),
        pygame.image.load("Undead executioner/Attack_6.png"),
        pygame.image.load("Undead executioner/Attack_7.png"),
        pygame.image.load("Undead executioner/Attack_8.png"),
        pygame.image.load("Undead executioner/Attack_9.png"),
        pygame.image.load("Undead executioner/Attack_10.png"),
        pygame.image.load("Undead executioner/Attack_11.png"),
        pygame.image.load("Undead executioner/Attack_12.png"),
        
    ],  
    'quieto': [
        pygame.image.load("Undead executioner/Idle_0.png"),
        pygame.image.load("Undead executioner/Idle_1.png"),
        pygame.image.load("Undead executioner/Idle_2.png"),
        pygame.image.load("Undead executioner/Idle_3.png")
    ], 

    'muerte': [
        pygame.image.load("Undead executioner/Death_0.png"),
        pygame.image.load("Undead executioner/Death_1.png"),
        pygame.image.load("Undead executioner/Death_2.png"),
        pygame.image.load("Undead executioner/Death_3.png"),
        pygame.image.load("Undead executioner/Death_4.png"),
        pygame.image.load("Undead executioner/Death_5.png"),
        pygame.image.load("Undead executioner/Death_6.png"),
        pygame.image.load("Undead executioner/Death_7.png"),
        pygame.image.load("Undead executioner/Death_8.png"),
        pygame.image.load("Undead executioner/Death_9.png"),
        pygame.image.load("Undead executioner/Death_10.png"),
        pygame.image.load("Undead executioner/Death_11.png"),
        pygame.image.load("Undead executioner/Death_12.png"),
        pygame.image.load("Undead executioner/Death_13.png"),
        pygame.image.load("Undead executioner/Death_14.png"),
        pygame.image.load("Undead executioner/Death_15.png"),
        pygame.image.load("Undead executioner/Death_16.png"),
        pygame.image.load("Undead executioner/Death_17.png"),
        pygame.image.load("Undead executioner/Death_18.png"),
        pygame.image.load("Undead executioner/Death_19.png"),
        pygame.image.load("Undead executioner/Death_20.png"),
        pygame.image.load("Undead executioner/Death_21.png"),
        pygame.image.load("Undead executioner/Death_22.png"),
        pygame.image.load("Undead executioner/Death_23.png"),
        pygame.image.load("Undead executioner/Death_24.png"),
        pygame.image.load("Undead executioner/Death_25.png"),
        pygame.image.load("Undead executioner/Death_26.png"),
        pygame.image.load("Undead executioner/Death_27.png"),
        pygame.image.load("Undead executioner/Death_28.png"),
        pygame.image.load("Undead executioner/Death_29.png"),
        pygame.image.load("Undead executioner/Death_30.png"),
        pygame.image.load("Undead executioner/Death_31.png"),
        pygame.image.load("Undead executioner/Death_32.png"),
        pygame.image.load("Undead executioner/Death_33.png"),
        pygame.image.load("Undead executioner/Death_34.png"),
        pygame.image.load("Undead executioner/Death_35.png"),
        pygame.image.load("Undead executioner/Death_36.png"),
        pygame.image.load("Undead executioner/Death_37.png"),
        pygame.image.load("Undead executioner/Death_38.png"),
        pygame.image.load("Undead executioner/Death_39.png"),
        pygame.image.load("Undead executioner/Death_40.png"),
        pygame.image.load("Undead executioner/Death_41.png"),
        pygame.image.load("Undead executioner/Death_42.png"),
        pygame.image.load("Undead executioner/Death_43.png"),
        pygame.image.load("Undead executioner/Death_44.png"),
        pygame.image.load("Undead executioner/Death_45.png"),
        pygame.image.load("Undead executioner/Death_46.png"),
        pygame.image.load("Undead executioner/Death_47.png"),
        pygame.image.load("Undead executioner/Death_48.png"),
        pygame.image.load("Undead executioner/Death_49.png"),
        pygame.image.load("Undead executioner/Death_50.png"),
        pygame.image.load("Undead executioner/Death_51.png"),
        pygame.image.load("Undead executioner/Death_52.png"),
        pygame.image.load("Undead executioner/Death_53.png"),
        pygame.image.load("Undead executioner/Death_54.png"),
        pygame.image.load("Undead executioner/Death_55.png")
    ],   
}